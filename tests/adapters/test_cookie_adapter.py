from jit.adapters.cookie_adapter import CookieAdapter
from jit.entities.http_cookie import HttpCookie


def test_from_mapping_empty():
    cookies = CookieAdapter.from_mapping(None)

    assert cookies == []


def test_from_mapping():
    cookies = CookieAdapter.from_mapping(
        {
            "session": "abc123",
            "user": "kevin",
        }
    )

    assert len(cookies) == 2

    assert cookies[0] == HttpCookie(
        name="session",
        value="abc123",
        domain=None,
    )

    assert cookies[1] == HttpCookie(
        name="user",
        value="kevin",
        domain=None,
    )


def test_from_mapping_empty_dict():
    cookies = CookieAdapter.from_mapping({})

    assert cookies == []


def test_from_list_empty():
    cookies = CookieAdapter.from_list(None)

    assert cookies == []


def test_from_list_empty_list():
    cookies = CookieAdapter.from_list([])

    assert cookies == []


def test_from_list_single_cookie():
    cookies = CookieAdapter.from_list(
        [
            {
                "name": "session",
                "value": "abc123",
                "domain": ".jumia.co.ke",
                "path": "/",
                "expires": 1234567890,
                "secure": True,
                "httpOnly": True,
                "sameSite": "Lax",
            }
        ]
    )

    assert len(cookies) == 1

    cookie = cookies[0]

    assert cookie.name == "session"
    assert cookie.value == "abc123"
    assert cookie.domain == ".jumia.co.ke"
    assert cookie.path == "/"
    assert cookie.expires == 1234567890
    assert cookie.secure is True
    assert cookie.http_only is True
    assert cookie.same_site == "Lax"


def test_from_list_defaults():
    cookies = CookieAdapter.from_list(
        [
            {
                "name": "test",
                "value": "123",
            }
        ]
    )

    cookie = cookies[0]

    assert cookie.domain is None
    assert cookie.path == "/"
    assert cookie.expires is None
    assert cookie.secure is False
    assert cookie.http_only is False
    assert cookie.same_site is None


def test_from_list_multiple():
    cookies = CookieAdapter.from_list(
        [
            {
                "name": "a",
                "value": "1",
            },
            {
                "name": "b",
                "value": "2",
            },
        ]
    )

    assert len(cookies) == 2

    assert cookies[0].name == "a"
    assert cookies[1].name == "b"


def test_returns_http_cookie_instances():
    cookies = CookieAdapter.from_mapping(
        {
            "session": "abc",
        }
    )

    assert all(isinstance(cookie, HttpCookie) for cookie in cookies)
