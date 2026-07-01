from __future__ import annotations

from pathlib import Path
from unittest.mock import AsyncMock, Mock, PropertyMock, patch

import pytest

from jit.browser.context import ContextManager


@pytest.fixture
def browser() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def context() -> AsyncMock:
    return AsyncMock()


def test_context_property_raises_before_start(
    browser: AsyncMock,
) -> None:
    manager = ContextManager(browser)

    with pytest.raises(RuntimeError):
        _ = manager.context


@pytest.mark.asyncio
async def test_start_creates_context(
    browser: AsyncMock,
    context: AsyncMock,
) -> None:
    browser.new_context.return_value = context

    manager = ContextManager(browser)

    with (
        patch(
            "jit.browser.context.Path.mkdir",
        ),
        patch.object(
            type(manager._session),
            "is_valid",
            new_callable=PropertyMock,
            return_value=False,
        ),
    ):
        result = await manager.start()

    assert result is context
    browser.new_context.assert_awaited_once()


@pytest.mark.asyncio
async def test_start_returns_existing_context(
    browser: AsyncMock,
) -> None:
    manager = ContextManager(browser)

    existing = AsyncMock()
    manager._context = existing

    result = await manager.start()

    assert result is existing
    browser.new_context.assert_not_called()


@pytest.mark.asyncio
async def test_start_uses_storage_state(
    browser: AsyncMock,
    context: AsyncMock,
) -> None:
    browser.new_context.return_value = context

    manager = ContextManager(browser)
    manager._session.state_path = Path("state.json")

    with (
        patch(
            "jit.browser.context.Path.mkdir",
        ),
        patch.object(
            type(manager._session),
            "is_valid",
            new_callable=PropertyMock,
            return_value=True,
        ),
    ):
        await manager.start()

    kwargs = browser.new_context.await_args.kwargs

    assert kwargs["storage_state"] == "state.json"


@pytest.mark.asyncio
async def test_start_without_storage_state(
    browser: AsyncMock,
    context: AsyncMock,
) -> None:
    browser.new_context.return_value = context

    manager = ContextManager(browser)

    with (
        patch(
            "jit.browser.context.Path.mkdir",
        ),
        patch.object(
            type(manager._session),
            "is_valid",
            new_callable=PropertyMock,
            return_value=False,
        ),
    ):
        await manager.start()

    kwargs = browser.new_context.await_args.kwargs

    assert kwargs["storage_state"] is None


@pytest.mark.asyncio
async def test_start_propagates_exception(
    browser: AsyncMock,
) -> None:
    browser.new_context.side_effect = RuntimeError("boom")

    manager = ContextManager(browser)

    with (
        patch(
            "jit.browser.context.Path.mkdir",
        ),
        patch.object(
            type(manager._session),
            "is_valid",
            new_callable=PropertyMock,
            return_value=False,
        ),pytest.raises(RuntimeError)
    ):
        await manager.start()


@pytest.mark.asyncio
async def test_new_page(
    browser: AsyncMock,
) -> None:
    manager = ContextManager(browser)

    manager._context = AsyncMock()

    page = Mock()
    manager._context.new_page.return_value = page

    result = await manager.new_page()

    assert result is page
    manager._context.new_page.assert_awaited_once()


@pytest.mark.asyncio
async def test_stop_saves_and_closes(
    browser: AsyncMock,
) -> None:
    manager = ContextManager(browser)

    context = AsyncMock()
    manager._context = context

    manager._session.save = AsyncMock()

    await manager.stop()

    manager._session.save.assert_awaited_once_with(context)
    context.close.assert_awaited_once()

    assert manager._context is None


@pytest.mark.asyncio
async def test_stop_handles_save_failure(
    browser: AsyncMock,
) -> None:
    manager = ContextManager(browser)

    context = AsyncMock()
    manager._context = context

    manager._session.save = AsyncMock(
        side_effect=RuntimeError,
    )

    await manager.stop()

    context.close.assert_awaited_once()

    assert manager._context is None


@pytest.mark.asyncio
async def test_stop_handles_close_failure(
    browser: AsyncMock,
) -> None:
    manager = ContextManager(browser)

    manager._context = AsyncMock()

    manager._session.save = AsyncMock()

    manager._context.close.side_effect = RuntimeError

    await manager.stop()

    manager._session.save.assert_awaited_once()
    assert manager._context is None


@pytest.mark.asyncio
async def test_aenter(
    browser: AsyncMock,
) -> None:
    manager = ContextManager(browser)

    start_mock = AsyncMock()

    with patch.object(
        manager,
        "start",
        start_mock,
    ):
        result = await manager.__aenter__()

    start_mock.assert_awaited_once()
    assert result is manager


@pytest.mark.asyncio
async def test_aexit(
    browser: AsyncMock,
) -> None:
    manager = ContextManager(browser)

    stop_mock = AsyncMock()

    with patch.object(
        manager,
        "stop",
        stop_mock,
    ):
        await manager.__aexit__(
            None,
            None,
            None,
        )

    stop_mock.assert_awaited_once()
