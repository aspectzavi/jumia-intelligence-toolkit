from jit.entities.http_cookie import HttpCookie
from jit.entities.http_header import HttpHeader
from jit.entities.http_request import HttpRequest


def create_request() -> HttpRequest:
    """
    Helper for creating a populated request.
    """

    request = HttpRequest(
        url="https://www.jumia.co.ke/api/products?page=1&limit=20",
        method="POST",
        resource_type="xhr",
        frame_url="https://www.jumia.co.ke/",
        is_navigation=False,
        post_data='{"query":"phone"}',
    )

    request.add_header(
        HttpHeader(
            "content-type",
            "application/json",
        )
    )

    request.add_header(
        HttpHeader(
            "authorization",
            "Bearer token",
        )
    )

    request.add_cookie(
        HttpCookie(
            name="session",
            value="abc123",
            domain=".jumia.co.ke",
        )
    )

    return request


def test_default_values():

    request = HttpRequest()

    assert request.method == "GET"
    assert request.url == ""
    assert request.headers == []
    assert request.cookies == []


def test_hostname():

    request = create_request()

    assert request.hostname == "www.jumia.co.ke"


def test_path():

    request = create_request()

    assert request.path == "/api/products"


def test_scheme():

    request = create_request()

    assert request.scheme == "https"


def test_query_parameters():

    request = create_request()

    assert request.query_parameters == {
        "page": ["1"],
        "limit": ["20"],
    }


def test_is_post():

    request = create_request()

    assert request.is_post


def test_is_get():

    request = HttpRequest()

    assert request.is_get


def test_content_type():

    request = create_request()

    assert (
        request.content_type
        == "application/json"
    )


def test_is_json():

    request = create_request()

    assert request.is_json


def test_is_api():

    request = create_request()

    assert request.is_api


def test_header_map():

    request = create_request()

    assert request.header_map == {
        "content-type": "application/json",
        "authorization": "Bearer token",
    }


def test_cookie_map():

    request = create_request()

    assert request.cookie_map == {
        "session": "abc123",
    }


def test_add_header():

    request = HttpRequest()

    request.add_header(
        HttpHeader(
            "accept",
            "*/*",
        )
    )

    assert len(request.headers) == 1


def test_add_cookie():

    request = HttpRequest()

    request.add_cookie(
        HttpCookie(
            name="user",
            value="123",
            domain="example.com",
        )
    )

    assert len(request.cookies) == 1


def test_to_dict():

    request = create_request()

    data = request.to_dict()

    assert data["url"] == request.url
    assert data["method"] == "POST"
    assert len(data["headers"]) == 2
    assert len(data["cookies"]) == 1


def test_from_dict():

    request = create_request()

    restored = HttpRequest.from_dict(
        request.to_dict()
    )

    assert restored.url == request.url
    assert restored.method == request.method
    assert len(restored.headers) == 2
    assert len(restored.cookies) == 1


def test_round_trip():

    request = create_request()

    restored = HttpRequest.from_dict(
        request.to_dict()
    )

    assert (
        restored.to_dict()
        == request.to_dict()
    )


def test_str():

    request = create_request()

    assert str(request) == (
        "POST "
        "https://www.jumia.co.ke/api/products?page=1&limit=20"
    )


def test_not_json():

    request = HttpRequest()

    request.add_header(
        HttpHeader(
            "content-type",
            "text/html",
        )
    )

    assert not request.is_json


def test_not_api():

    request = HttpRequest(
        url="https://www.jumia.co.ke/about"
    )

    assert not request.is_api


def test_empty_query_parameters():

    request = HttpRequest(
        url="https://www.jumia.co.ke/"
    )

    assert request.query_parameters == {}


def test_cookie_map_empty():

    request = HttpRequest()

    assert request.cookie_map == {}


def test_header_map_empty():

    request = HttpRequest()

    assert request.header_map == {}
