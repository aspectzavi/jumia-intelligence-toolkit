from __future__ import annotations

from jit.playwright.playwright_capture import PlaywrightCapture


def test_capture_initial_state() -> None:
    capture = PlaywrightCapture()

    assert capture.started is False
    assert capture.browser is None
    assert capture.context is None
    assert capture.page is None


def test_capture_start() -> None:
    capture = PlaywrightCapture()

    capture.start()

    assert capture.started is True
    assert capture.browser is not None
    assert capture.context is not None
    assert capture.page is not None

    capture.stop()


def test_capture_stop() -> None:
    capture = PlaywrightCapture()

    capture.start()
    capture.stop()

    assert capture.started is False
    assert capture.browser is None
    assert capture.context is None
    assert capture.page is None


def test_mapper_exists() -> None:
    capture = PlaywrightCapture()

    assert capture.mapper is not None


def test_event_handlers_exist() -> None:
    capture = PlaywrightCapture()

    assert capture.handlers is not None
