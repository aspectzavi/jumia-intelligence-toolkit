from __future__ import annotations

from typing import Protocol

from jit.playwright.response_mapper import ResponseMapper


class FakeResponse:
    def __init__(self) -> None:
        self.status = 200
        self.status_text = "OK"
        self.url = "https://api.example.com/products"

        self.headers = {
            "content-type": "application/json",
        }


def test_map_response():
    response = FakeResponse()

    result = ResponseMapper.map(
        request_id="abc123",
        response=response,
    )

    assert result.request_id == "abc123"
    assert result.status == 200
    assert result.status_text == "OK"
    assert result.url == response.url


def test_headers_are_mapped():
    response = FakeResponse()

    result = ResponseMapper.map(
        request_id="abc123",
        response=response,
    )

    assert (
        result.header_map["content-type"]
        == "application/json"
    )


class ResponseLike(Protocol):
    status: int
    status_text: str
    url: str
    headers: dict[str, str]
