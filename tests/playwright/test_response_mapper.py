from __future__ import annotations

from jit.playwright.request_mapper import RequestLike
from jit.playwright.response_mapper import (
    ResponseLike,
    ResponseMapper,
)


class FakeRequest:
    def __init__(self) -> None:
        self._url = "https://api.example.com/products"

    @property
    def url(self) -> str:
        return self._url

    @property
    def method(self) -> str:
        return "GET"

    @property
    def resource_type(self) -> str:
        return "xhr"

    @property
    def headers(self) -> dict[str, str]:
        return {}

    @property
    def post_data(self) -> str | None:
        return None


class FakeResponse:
    def __init__(self) -> None:
        self._status = 200
        self._status_text = "OK"
        self._url = "https://api.example.com/products"

        self._headers = {
            "content-type": "application/json",
        }

        self._request = FakeRequest()

    @property
    def status(self) -> int:
        return self._status

    @property
    def status_text(self) -> str:
        return self._status_text

    @property
    def url(self) -> str:
        return self._url

    @property
    def headers(self) -> dict[str, str]:
        return self._headers

    @property
    def request(self) -> RequestLike:
        return self._request


def test_map_basic_response() -> None:
    response: ResponseLike = FakeResponse()

    result = ResponseMapper.map(
        request_id="request-123",
        response=response,
    )

    assert result.request_id == "request-123"
    assert result.status == 200
    assert result.status_text == "OK"
    assert result.url == response.url


def test_headers_are_mapped() -> None:
    response: ResponseLike = FakeResponse()

    result = ResponseMapper.map(
        request_id="request-123",
        response=response,
    )

    assert result.header_map["content-type"] == "application/json"
