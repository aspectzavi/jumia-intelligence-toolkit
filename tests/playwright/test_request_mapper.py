from __future__ import annotations

from jit.playwright.request_mapper import RequestLike, RequestMapper


class FakeRequest(RequestLike):
    def __init__(self) -> None:
        self.url = "https://api.example.com/products"
        self.method = "POST"
        self.resource_type = "xhr"

        self.headers = {
            "content-type": "application/json",
        }

        self.post_data = '{"name":"Laptop"}'


def test_map_basic_request() -> None:
    request: RequestLike = FakeRequest()

    result = RequestMapper.map(request)

    assert result.url == request.url
    assert result.method == "POST"
    assert result.resource_type == "xhr"


def test_headers_are_mapped() -> None:
    request: RequestLike = FakeRequest()

    result = RequestMapper.map(request)

    assert result.header_map["content-type"] == "application/json"


def test_post_data_is_preserved() -> None:
    request: RequestLike = FakeRequest()

    result = RequestMapper.map(request)

    assert result.post_data == '{"name":"Laptop"}'
