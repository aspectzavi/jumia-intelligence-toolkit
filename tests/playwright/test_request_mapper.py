from __future__ import annotations

from jit.playwright.request_mapper import (
    RequestLike,
    RequestMapper,
)


class FakeRequest:
    def __init__(self) -> None:
        self._url = "https://api.example.com/products"
        self._method = "GET"
        self._resource_type = "xhr"

        self._headers = {
            "authorization": "Bearer token",
        }

        self._post_data = '{"page":1}'

    @property
    def url(self) -> str:
        return self._url

    @property
    def method(self) -> str:
        return self._method

    @property
    def resource_type(self) -> str:
        return self._resource_type

    @property
    def headers(self) -> dict[str, str]:
        return self._headers

    @property
    def post_data(self) -> str | None:
        return self._post_data


def test_map_basic_request() -> None:
    request: RequestLike = FakeRequest()

    result = RequestMapper.map(request)

    assert result.method == "GET"
    assert result.url == "https://api.example.com/products"


def test_headers_are_mapped() -> None:
    request: RequestLike = FakeRequest()

    result = RequestMapper.map(request)

    assert result.header_map["authorization"] == "Bearer token"


def test_post_data_is_preserved() -> None:
    request: RequestLike = FakeRequest()

    result = RequestMapper.map(request)

    assert result.body == '{"page":1}'
