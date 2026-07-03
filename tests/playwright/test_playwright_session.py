from __future__ import annotations

from jit.playwright.playwright_session import PlaywrightSession


def test_initial_state():
    session = PlaywrightSession()

    assert session.started is False
    assert session.browser is None
    assert session.context is None
    assert session.page is None


def test_mark_started():
    session = PlaywrightSession()

    session._started()

    assert session.started is True


def test_mark_stopped():
    session = PlaywrightSession()

    session._started()
    session._stopped()

    assert session.started is False
