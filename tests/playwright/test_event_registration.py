from __future__ import annotations

from jit.playwright.playwright_capture import PlaywrightCapture


def test_register_events() -> None:
    capture = PlaywrightCapture()

    capture.start()

    assert capture.page is not None

    capture.register_events()

    capture.stop()
