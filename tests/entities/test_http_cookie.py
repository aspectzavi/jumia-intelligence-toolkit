from __future__ import annotations

from jit.entities.http_cookie import HttpCookie


def test_create_cookie() -> None:
    cookie = HttpCookie(
        name="session",
        value="abc123",
        domain=".jumia.co.ke",
    )

    assert cookie.name == "session"
    assert cookie.value == "abc123"
    assert cookie.domain == ".jumia.co.ke"
    assert cookie.path == "/"
    assert cookie.secure is False
    assert cookie.http_only is False


def test_to_dict() -> None:
    cookie = HttpCookie(
        name="lang",
        value="en",
        domain="jumia.co.ke",
        secure=True,
        http_only=True,
        same_site="Lax",
    )

    assert cookie.to_dict() == {
        "name": "lang",
        "value": "en",
        "domain": "jumia.co.ke",
        "path": "/",
        "expires": None,
        "secure": True,
        "http_only": True,
        "same_site": "Lax",
    }


def test_from_dict() -> None:
    cookie = HttpCookie.from_dict(
        {
            "name": "token",
            "value": "xyz",
            "domain": ".jumia.co.ke",
            "path": "/",
            "expires": None,
            "secure": True,
            "http_only": True,
            "same_site": "Lax",
        }
    )

    assert cookie.name == "token"
    assert cookie.value == "xyz"
    assert cookie.domain == ".jumia.co.ke"
    assert cookie.path == "/"
    assert cookie.secure is True
    assert cookie.http_only is True
    assert cookie.same_site == "Lax"


def test_cookie_not_expired() -> None:
    cookie = HttpCookie(
        name="test",
        value="1",
        domain="example.com",
    )

    assert cookie.is_expired(9999999999) is False


def test_cookie_expired() -> None:
    cookie = HttpCookie(
        name="test",
        value="1",
        domain="example.com",
        expires=1000,
    )

    assert cookie.is_expired(1000) is True
    assert cookie.is_expired(2000) is True


def test_string_representation() -> None:
    cookie = HttpCookie(
        name="session",
        value="abc123",
        domain=".jumia.co.ke",
        path="/",
    )

    assert (
        str(cookie)
        == "session=abc123; Domain=.jumia.co.ke; Path=/"
    )
