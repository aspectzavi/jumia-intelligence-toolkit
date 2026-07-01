from unittest.mock import AsyncMock, Mock

import pytest

from jit.adapters.playwright_response_adapter import (
    PlaywrightResponseAdapter,
)


@pytest.mark.asyncio
async def test_basic_response():
    response = Mock()

    response.url = "https://www.jumia.co.ke/api/products"
    response.status = 200
    response.status_text = "OK"

    response.all_headers = AsyncMock(
        return_value={
            "Content-Type": "application/json",
        }
    )

    response.body = AsyncMock(return_value=b'{"success":true}')

    result = await PlaywrightResponseAdapter.from_playwright(
        response,
        request_id="123",
    )

    assert result.request_id == "123"
    assert result.status == 200
    assert result.status_text == "OK"
    assert result.url == response.url


@pytest.mark.asyncio
async def test_headers_are_converted():
    response = Mock()

    response.url = "https://example.com"
    response.status = 200
    response.status_text = "OK"

    response.all_headers = AsyncMock(
        return_value={
            "Content-Type": "application/json",
            "Content-Length": "150",
        }
    )

    response.body = AsyncMock(return_value=b"{}")

    result = await PlaywrightResponseAdapter.from_playwright(
        response,
        request_id="1",
    )

    assert result.headers.content_type == "application/json"
    assert result.headers.content_length == 150


@pytest.mark.asyncio
async def test_json_response():
    response = Mock()

    response.url = "https://example.com/api"
    response.status = 200
    response.status_text = "OK"

    response.all_headers = AsyncMock(
        return_value={
            "Content-Type": "application/json",
        }
    )

    response.body = AsyncMock(return_value=b'{"id":1}')

    result = await PlaywrightResponseAdapter.from_playwright(
        response,
        request_id="1",
    )

    assert result.is_json


@pytest.mark.asyncio
async def test_html_response():
    response = Mock()

    response.url = "https://example.com"
    response.status = 200
    response.status_text = "OK"

    response.all_headers = AsyncMock(
        return_value={
            "Content-Type": "text/html",
        }
    )

    response.body = AsyncMock(return_value=b"<html></html>")

    result = await PlaywrightResponseAdapter.from_playwright(
        response,
        request_id="1",
    )

    assert result.is_html


@pytest.mark.asyncio
async def test_binary_body():
    response = Mock()

    response.url = "https://example.com/image.png"
    response.status = 200
    response.status_text = "OK"

    response.all_headers = AsyncMock(
        return_value={
            "Content-Type": "image/png",
        }
    )

    binary = b"\x89PNG\r\n\x1a\n"

    response.body = AsyncMock(return_value=binary)

    result = await PlaywrightResponseAdapter.from_playwright(
        response,
        request_id="1",
    )

    assert result.body == binary
    assert result.is_image


@pytest.mark.asyncio
async def test_empty_body():
    response = Mock()

    response.url = "https://example.com"
    response.status = 204
    response.status_text = "No Content"

    response.all_headers = AsyncMock(return_value={})

    response.body = AsyncMock(return_value=b"")

    result = await PlaywrightResponseAdapter.from_playwright(
        response,
        request_id="1",
    )

    assert result.body == b""


@pytest.mark.asyncio
async def test_body_exception_returns_none():
    response = Mock()

    response.url = "https://example.com"
    response.status = 200
    response.status_text = "OK"

    response.all_headers = AsyncMock(return_value={})

    response.body = AsyncMock(side_effect=RuntimeError())

    result = await PlaywrightResponseAdapter.from_playwright(
        response,
        request_id="1",
    )

    assert result.body is None


@pytest.mark.asyncio
async def test_content_length_is_extracted():
    response = Mock()

    response.url = "https://example.com"
    response.status = 200
    response.status_text = "OK"

    response.all_headers = AsyncMock(
        return_value={
            "Content-Length": "512",
        }
    )

    response.body = AsyncMock(return_value=b"x")

    result = await PlaywrightResponseAdapter.from_playwright(
        response,
        request_id="1",
    )

    assert result.content_length == 512


@pytest.mark.asyncio
async def test_request_id_is_preserved():
    response = Mock()

    response.url = "https://example.com"
    response.status = 200
    response.status_text = "OK"

    response.all_headers = AsyncMock(return_value={})

    response.body = AsyncMock(return_value=b"")

    result = await PlaywrightResponseAdapter.from_playwright(
        response,
        request_id="request-abc",
    )

    assert result.request_id == "request-abc"


@pytest.mark.asyncio
async def test_timing_is_created():
    response = Mock()

    response.url = "https://example.com"
    response.status = 200
    response.status_text = "OK"

    response.all_headers = AsyncMock(return_value={})

    response.body = AsyncMock(return_value=b"")

    result = await PlaywrightResponseAdapter.from_playwright(
        response,
        request_id="1",
    )

    assert result.timing is not None
