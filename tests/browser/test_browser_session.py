from __future__ import annotations

from jit.browser.browser_options import BrowserOptions
from jit.browser.browser_session import BrowserSession


def test_session_initial_state():
    session = BrowserSession()

    assert session.is_running is False


def test_start_session():
    session = BrowserSession()

    session.start()

    assert session.is_running is True


def test_stop_session():
    session = BrowserSession()

    session.start()
    session.stop()

    assert session.is_running is False


def test_options_are_assigned():
    options = BrowserOptions(
        headless=False,
    )

    session = BrowserSession(options)

    assert session.options is options
