from unittest.mock import AsyncMock, Mock

import pytest

from jit.adapters.playwright_request_adapter import (
    PlaywrightRequestAdapter,
)


@pytest.mark.asyncio
async def test_basic_request():
    request = Mock()

    request.url = "https://www.jumia.co.ke/api/products"
    request.method = "GET"
    request.resource_type = "xhr"

    request.frame = Mock()
    request.frame.url = "https://www.jumia.co.ke/"

    request.post_data = None

    request.is_navigation_request.return_value = False

    request.all_headers = AsyncMock(
        return_value={
            "content-type": "application/json",
        }
    )

    result = await PlaywrightRequestAdapter.from_playwright(request)

    assert result.url == request.url
    assert result.method == "GET"
    assert result.resource_type == "xhr"


@pytest.mark.asyncio
async def test_headers_are_converted():
    request = Mock()

    request.url = "https://example.com"
    request.method = "GET"
    request.resource_type = "document"

    request.frame = Mock()
    request.frame.url = "https://example.com"

    request.post_data = None

    request.is_navigation_request.return_value = False

    request.all_headers = AsyncMock(
        return_value={
            "Content-Type": "application/json",
            "User-Agent": "Playwright",
        }
    )

    result = await PlaywrightRequestAdapter.from_playwright(request)

    assert result.headers.content_type == "application/json"

    assert result.headers.user_agent == "Playwright"


@pytest.mark.asyncio
async def test_cookie_header_is_parsed():
    request = Mock()

    request.url = "https://example.com"
    request.method = "GET"
    request.resource_type = "xhr"

    request.frame = Mock()
    request.frame.url = "https://example.com"

    request.post_data = None

    request.is_navigation_request.return_value = False

    request.all_headers = AsyncMock(return_value={"Cookie": ("session=abc; theme=dark")})

    result = await PlaywrightRequestAdapter.from_playwright(request)

    assert len(result.cookies) == 2

    assert result.cookies[0].name == "session"
    assert result.cookies[0].value == "abc"

    assert result.cookies[1].name == "theme"


@pytest.mark.asyncio
async def test_navigation_request():
    request = Mock()

    request.url = "https://example.com"
    request.method = "GET"
    request.resource_type = "document"

    request.frame = Mock()
    request.frame.url = "https://example.com"

    request.post_data = None

    request.is_navigation_request.return_value = True

    request.all_headers = AsyncMock(return_value={})

    result = await PlaywrightRequestAdapter.from_playwright(request)

    assert result.is_navigation is True


@pytest.mark.asyncio
async def test_post_request():
    request = Mock()

    request.url = "https://example.com/api"

    request.method = "POST"

    request.resource_type = "fetch"

    request.frame = Mock()
    request.frame.url = "https://example.com"

    request.post_data = '{"id":1}'

    request.is_navigation_request.return_value = False

    request.all_headers = AsyncMock(
        return_value={
            "Content-Type": "application/json",
        }
    )

    result = await PlaywrightRequestAdapter.from_playwright(request)

    assert result.post_data == '{"id":1}'

    assert result.is_post
