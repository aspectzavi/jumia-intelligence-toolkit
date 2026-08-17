# Interaction Layer — Design

## Status

Design proposal. Not yet implemented. Written after live-fire validation
against `https://www.jumia.co.ke` (see git history around
`fix(network): await in-flight handlers...`) showed that a plain
navigate-and-wait capture returns **zero JSON API responses** — Jumia's
homepage is server-side rendered, and the real product/search/category API
traffic only fires on user interaction (search, click, scroll, pagination).

This is new scope. It was not part of the original engineering handoff.

## Problem

`CaptureRunner.capture()` today does exactly one thing on the page:
`goto(url)`, then wait for network idle. That's sufficient for
API-first / SPA sites where the initial page load itself triggers the
real API calls. It is not sufficient for SSR sites like Jumia, where
meaningful API traffic only appears after a user does something.

## Goals

- Generic, reusable interaction primitives — no Jumia-specific logic in
  the core engine. Mirrors the existing rule that site-specific behavior
  belongs in a "site adapter," not the generic discovery engine.
- Composable into named scripts, so a capture can say "run this sequence
  of actions" without the caller hand-writing Playwright code.
- Safe by default. This executes real actions against a real third-party
  site. Accidental form submissions, checkout flows, or purchases are an
  unacceptable failure mode for a discovery tool.
- Observable. Every step's outcome (succeeded/failed/skipped) and the
  network traffic it triggered should be reported, not silently absorbed.
- Zero duplication with `CaptureRunner` / `NetworkInterceptor` / capture
  responsibilities already built.

## Non-goals (first version)

- No login/authentication automation. Authenticated flows should reuse
  the existing `storage_state.json` session mechanism, not have the
  interaction engine type in credentials.
- No AI-driven/adaptive interaction ("figure out how to search"). Scripts
  are explicit, deterministic step sequences supplied by the caller.
- No cross-origin navigation following by default.

## Where it lives

New top-level package, parallel to `browser/`, `capture/`, `network/`:

```text
jit/interaction/
├── __init__.py
├── steps.py       # InteractionStep primitives (pure data, no Playwright)
├── script.py       # InteractionScript: named, ordered list of steps
├── engine.py        # InteractionEngine: executes a script against a Page
├── result.py        # StepResult / InteractionResult
└── guardrails.py    # denylist checks, step/time budgets
```

Site-specific scripts (a Jumia search flow, category browse, etc.) do
**not** live here. Per the existing site-adapter boundary
(`jit/sites/jumia/...`, not yet built), a reusable Jumia search scenario
would live at `jit/sites/jumia/scenarios.py` and simply construct an
`InteractionScript` out of the generic primitives below. The engine
itself never knows what "Jumia" is.

## Core abstractions

### `InteractionStep` (steps.py)

Frozen dataclasses, pure data — no Playwright objects — so a script can
be expressed as JSON/YAML and round-tripped, matching the project's
existing exporter/serializer conventions.

```python
@dataclass(frozen=True, slots=True)
class Click:
    selector: str
    timeout_ms: int = 5000
    optional: bool = False   # False = failure aborts the script

@dataclass(frozen=True, slots=True)
class Fill:
    selector: str
    value: str
    timeout_ms: int = 5000
    optional: bool = False

@dataclass(frozen=True, slots=True)
class PressKey:
    key: str
    selector: str | None = None

@dataclass(frozen=True, slots=True)
class Scroll:
    times: int = 1
    pixels: int = 800
    delay_ms: int = 300

@dataclass(frozen=True, slots=True)
class WaitForSelector:
    selector: str
    timeout_ms: int = 5000

@dataclass(frozen=True, slots=True)
class WaitForNetworkIdle:
    timeout_ms: int = 3000

@dataclass(frozen=True, slots=True)
class WaitMs:
    duration_ms: int

Step = Click | Fill | PressKey | Scroll | WaitForSelector | WaitForNetworkIdle | WaitMs
```

Deliberately excluded from the primitive set: nothing that submits a
form outright, nothing that types into password fields, nothing that
navigates cross-origin. `Click`/`Fill` are still generic enough to hit a
"Buy now" button if a script is misconfigured — see Guardrails below for
how that's mitigated, since it can't be prevented structurally without
also blocking legitimate "Add to cart to observe the API call" use cases.

### `InteractionScript` (script.py)

```python
@dataclass(slots=True)
class InteractionScript:
    name: str
    steps: list[Step]
    description: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> InteractionScript: ...
    def to_dict(self) -> dict[str, Any]: ...
```

### `InteractionEngine` (engine.py)

The only piece that touches a live Playwright `Page`.

```python
class InteractionEngine:
    async def run(
        self,
        page: Page,
        script: InteractionScript,
        *,
        drain: Callable[[], Awaitable[None]] | None = None,
        budget: StepBudget = StepBudget(),
    ) -> InteractionResult:
        ...
```

Behavior:
- Executes steps in order.
- After each step, waits briefly for network idle (bounded timeout, not
  the long default), and — critically — calls `drain()` if supplied,
  before moving to the next step. This reuses the exact fix just shipped
  for the capture race: interaction steps trigger new in-flight
  request/response handler tasks, and those need to be drained before
  the *next* action fires, not just once at the very end.
- A step with `optional=False` (the default) that fails aborts the
  script; the failure is recorded, not raised past the engine.
- A step with `optional=True` that fails is recorded and execution
  continues.
- Enforces `StepBudget` (see Guardrails) — max steps, max total wall
  time.

### `InteractionResult` / `StepResult` (result.py)

```python
@dataclass(slots=True)
class StepResult:
    step: Step
    succeeded: bool
    error: str | None
    duration_ms: float
    requests_triggered: int   # recorder count delta across this step

@dataclass(slots=True)
class InteractionResult:
    script_name: str
    step_results: list[StepResult]
    aborted: bool

    @property
    def succeeded_count(self) -> int: ...
    @property
    def total_requests_triggered(self) -> int: ...
```

`requests_triggered` is computed by snapshotting
`NetworkRecorder.request_count` before and after each step — no new
correlation mechanism needed, reuses what `CaptureSession` already
exposes.

## Guardrails (guardrails.py)

This is the part that matters most, since the engine executes real
actions against a real third-party site:

- **Step budget.** Default max 25 steps and 60s total wall time per
  script. Configurable, but bounded by default so a bad script can't run
  indefinitely or hammer a site.
- **Purchase/checkout denylist (soft).** Before executing a `Click` or
  `Fill`, the engine checks the target element's visible text / aria-label
  / name against a small denylist of keywords (`buy now`, `checkout`,
  `place order`, `pay`, `confirm purchase`, `add card`, ...). A match logs
  a warning and skips the step unless the step explicitly sets
  `force=True`. This is not foolproof — text-based matching can be wrong
  in either direction — but it removes the most common accidental-purchase
  failure mode during exploratory scripting, and it errs toward skipping
  rather than silently proceeding.
- **Same-origin by default.** If a step's resulting navigation would leave
  the original target's origin (e.g., an ad click, an external link), the
  engine stops following it and records the step as skipped, unless the
  script explicitly opts in via `allow_cross_origin=True` at the script
  level.
- **No credential fields.** `Fill` refuses (raises at script-construction
  time, not at runtime) if `selector` matches common password-field
  patterns (`input[type=password]`), forcing authenticated flows through
  the existing `storage_state.json` session mechanism instead.

None of this makes the engine safe to point at an arbitrary unknown site
unsupervised — it reduces the blast radius of common mistakes, it doesn't
eliminate the need for a human to review a script before running it
against a real site, especially one they don't operate.

## Integration points

### `CaptureRunner.capture()`

Gains one new optional parameter. No existing behavior changes when it's
omitted.

```python
async def capture(
    self,
    url: str,
    *,
    wait_until: WaitUntil = "networkidle",
    script: InteractionScript | None = None,
) -> CaptureSession:

    async with BrowserManager() as browser, browser.new_context() as context:
        capture = CaptureSession()
        await capture.attach(context.context)

        page = await context.new_page()
        await page.goto(url, wait_until=wait_until)
        await capture.drain()

        if script is not None:
            result = await InteractionEngine().run(
                page,
                script,
                drain=capture.drain,
            )
            capture.set_interaction_result(result)

        await capture.drain()
        capture.process()
        return capture
```

`CaptureSession` gains `interaction_result: InteractionResult | None`
(default `None`) so downstream consumers — the CLI — can report on it
without `CaptureRunner` needing to return two different types.

### `DiscoveryPipeline.discover()`

Forwards `script` straight through to `CaptureRunner.capture()`. No new
responsibility — matches the orchestration-only principle the pipeline
was already built around.

### CLI

Two levels of ergonomics, both living in `cli/discover.py` /
`cli/main.py` — script parsing is a CLI concern, not an engine concern:

1. **Ad-hoc flags** for simple one-off scripts, assembled into an
   `InteractionScript` at the CLI layer:

   ```bash
   jit discover https://www.jumia.co.ke \
     --click "input[name=q]" \
     --fill "input[name=q]=iphone" \
     --press Enter \
     --export openapi.yaml
   ```

2. **Script files** for anything more than a couple of steps, loaded via
   `InteractionScript.from_dict()`:

   ```bash
   jit discover https://www.jumia.co.ke --script jumia-search.yaml
   ```

   Script files are shareable, reviewable, and diffable — an important
   property for something that executes real actions, since a reviewer
   can read exactly what a script will do before anyone runs it.

### Reporting

New section in the existing CLI summary (`discover.py` already prints
Capture / Discovery / Analysis / Export sections):

```text
Interaction
-----------
Script:     jumia-search
Steps:      4/4 succeeded
Triggered:  12 new requests, 3 new endpoints
```

## Testing strategy

- `InteractionEngine` tested against a **mocked** Playwright `Page` —
  same pattern already used for `NetworkInterceptor`'s tests. No real
  browser needed for unit coverage.
- Planned cases: step success; optional-step failure continues; required-
  step failure aborts and is recorded; step budget enforcement; denylist
  warning skips a step unless `force=True`; cross-origin navigation is
  blocked by default.
- Real-browser validation stays manual/live against jumia.co.ke (as done
  this session for the capture-race fix), not part of CI — CI has no
  business hitting a real third-party site.

## Suggested build order

1. `steps.py` + `script.py` — pure data, zero risk, trivial to test.
2. `guardrails.py` — budget + denylist logic, pure functions, no browser.
3. `engine.py` against a mocked `Page` — the core logic, fully unit-
   testable without a real browser.
4. Wire `CaptureRunner.capture(script=...)` + `CaptureSession
   .interaction_result` — small, additive, doesn't touch existing paths
   when `script` is omitted.
5. `DiscoveryPipeline.discover(script=...)` passthrough.
6. CLI ad-hoc flags, then `--script <file>` loader.
7. Live validation against jumia.co.ke with a real search scenario;
   iterate on timing/guardrails based on what actually happens live —
   this is exactly the kind of thing that behaves differently on a real
   site than in a mock.
8. Only after the generic engine is proven: a Jumia-specific scenario
   under `jit/sites/jumia/scenarios.py`, per the existing site-adapter
   boundary. Not part of this design.
