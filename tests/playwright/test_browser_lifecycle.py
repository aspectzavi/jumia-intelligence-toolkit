from __future__ import annotations

from jit.playwright.playwright_capture import PlaywrightCapture


def test_start_creates_browser() -> None:
    capture = PlaywrightCapture()

    capture.start()

    assert capture.browser is not None
    assert capture.context is not None
    assert capture.page is not None

    capture.stop()


def test_stop_closes_browser() -> None:
    capture = PlaywrightCapture()

    capture.start()
    capture.stop()

    assert capture.started is False
    assert capture.browser is None
    assert capture.context is None
    assert capture.page is None
