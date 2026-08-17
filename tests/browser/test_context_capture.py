from __future__ import annotations

from unittest.mock import AsyncMock

import pytest
from playwright.async_api import Browser, BrowserContext, Page

from jit.browser.context import ContextManager
from jit.network.capture import CaptureSession


@pytest.mark.asyncio
async def test_capture_session_created() -> None:
    browser = AsyncMock(spec=Browser)

    manager = ContextManager(browser)

    assert isinstance(
        manager.capture,
        CaptureSession,
    )


@pytest.mark.asyncio
async def test_new_page_attaches_capture() -> None:
    browser = AsyncMock(spec=Browser)
    context = AsyncMock(spec=BrowserContext)
    page = AsyncMock(spec=Page)

    context.new_page.return_value = page

    manager = ContextManager(browser)
    manager._context = context

    manager.capture.attach = AsyncMock()

    created_page = await manager.new_page()

    assert created_page is page

    manager.capture.attach.assert_awaited_once_with(
        page,
    )


@pytest.mark.asyncio
async def test_new_page_returns_page() -> None:
    browser = AsyncMock(spec=Browser)
    context = AsyncMock(spec=BrowserContext)
    page = AsyncMock(spec=Page)

    context.new_page.return_value = page

    manager = ContextManager(browser)
    manager._context = context

    manager.capture.attach = AsyncMock()

    created_page = await manager.new_page()

    assert created_page is page


@pytest.mark.asyncio
async def test_same_capture_session_reused() -> None:
    browser = AsyncMock(spec=Browser)
    context = AsyncMock(spec=BrowserContext)
    page = AsyncMock(spec=Page)

    context.new_page.return_value = page

    manager = ContextManager(browser)
    manager._context = context

    manager.capture.attach = AsyncMock()

    first = manager.capture

    await manager.new_page()
    await manager.new_page()

    second = manager.capture

    assert first is second

    assert manager.capture.attach.await_count == 2
