from __future__ import annotations

from jit.entities.http_cookie import HttpCookie
from jit.serializers.http_cookie_serializer import HttpCookieSerializer


def test_to_dict() -> None:
    cookie = HttpCookie(
        name="session",
        value="abc123",
        domain="jumia.co.ke",
        secure=True,
    )

    result = HttpCookieSerializer.to_dict(cookie)

    assert result["name"] == "session"
    assert result["value"] == "abc123"
    assert result["domain"] == "jumia.co.ke"
    assert result["secure"] is True


def test_from_dict() -> None:
    data = {
        "name": "session",
        "value": "abc123",
        "domain": "jumia.co.ke",
        "path": "/",
        "expires": None,
        "secure": True,
        "http_only": False,
        "same_site": None,
    }

    cookie = HttpCookieSerializer.from_dict(data)

    assert cookie.name == "session"
    assert cookie.value == "abc123"
    assert cookie.domain == "jumia.co.ke"
    assert cookie.secure is True


def test_round_trip() -> None:
    original = HttpCookie(
        name="token",
        value="xyz",
        domain="api.jumia.co.ke",
        http_only=True,
    )

    restored = HttpCookieSerializer.from_dict(
        HttpCookieSerializer.to_dict(original)
    )

    assert restored == original
