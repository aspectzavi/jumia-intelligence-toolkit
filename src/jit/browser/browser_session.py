from __future__ import annotations

from jit.browser.browser_options import BrowserOptions


class BrowserSession:
    """
    Base browser session.

    Concrete implementations (Playwright, Selenium, CDP)
    will inherit from this class.
    """

    def __init__(
        self,
        options: BrowserOptions | None = None,
    ) -> None:
        self.options = options or BrowserOptions()
        self.started = False

    def start(self) -> None:
        self.started = True

    def stop(self) -> None:
        self.started = False

    @property
    def is_running(self) -> bool:
        return self.started
