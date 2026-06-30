from jit.entities.http_cookie import HttpCookie


def test_create_cookie():
    cookie = HttpCookie(
        name="session",
        value="abc123",
        domain=".jumia.co.ke",
    )

    assert cookie.name == "session"
    assert cookie.value == "abc123"
    assert cookie.domain == ".jumia.co.ke"


def test_to_dict():
    cookie = HttpCookie(
        name="lang",
        value="en",
        domain="jumia.co.ke",
    )

    data = cookie.to_dict()

    assert data["name"] == "lang"
    assert data["value"] == "en"
    assert data["domain"] == "jumia.co.ke"


def test_from_dict():
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

    assert cookie.secure
    assert cookie.http_only
    assert cookie.same_site == "Lax"


def test_cookie_not_expired():
    cookie = HttpCookie(
        name="test",
        value="1",
        domain="example.com",
    )

    assert cookie.is_expired(9999999999) is False
