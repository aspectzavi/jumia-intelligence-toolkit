from unittest.mock import AsyncMock, Mock, patch

import pytest

from jit.entities.http_request import HttpRequest
from jit.entities.http_response import HttpResponse
from jit.network.interceptor import NetworkInterceptor
from jit.network.recorder import NetworkRecorder


@pytest.mark.asyncio
async def test_attach_registers_request_handler():
    recorder = NetworkRecorder()

    interceptor = NetworkInterceptor(recorder)

    page = Mock()

    await interceptor.attach(page)

    page.on.assert_any_call(
        "request",
        interceptor._handle_request,
    )


@pytest.mark.asyncio
async def test_attach_registers_response_handler():
    recorder = NetworkRecorder()

    interceptor = NetworkInterceptor(recorder)

    page = Mock()

    await interceptor.attach(page)

    page.on.assert_any_call(
        "response",
        interceptor._handle_response,
    )


@pytest.mark.asyncio
@patch(
    "jit.network.interceptor.PlaywrightRequestAdapter.from_playwright",
    new_callable=AsyncMock,
)
async def test_handle_request_records_request(
    adapter,
):
    recorder = Mock()

    interceptor = NetworkInterceptor(recorder)

    entity = HttpRequest(
        url="https://example.com",
    )

    adapter.return_value = entity

    request = Mock()

    await interceptor._handle_request(request)

    adapter.assert_awaited_once_with(request)

    recorder.record_request.assert_called_once_with(entity)


@pytest.mark.asyncio
@patch(
    "jit.network.interceptor.PlaywrightResponseAdapter.from_playwright",
    new_callable=AsyncMock,
)
async def test_handle_response_records_response(
    adapter,
):
    recorder = Mock()

    interceptor = NetworkInterceptor(recorder)

    entity = HttpResponse(
        request_id="1",
        status=200,
    )

    adapter.return_value = entity

    response = Mock()
    response.request = Mock()

    await interceptor._handle_response(response)

    adapter.assert_awaited_once()

    recorder.record_response.assert_called_once_with(entity)


@pytest.mark.asyncio
@patch(
    "jit.network.interceptor.PlaywrightRequestAdapter.from_playwright",
    new_callable=AsyncMock,
)
async def test_request_adapter_called_once(
    adapter,
):
    recorder = Mock()

    interceptor = NetworkInterceptor(recorder)

    adapter.return_value = HttpRequest()

    request = Mock()

    await interceptor._handle_request(request)

    assert adapter.await_count == 1


@pytest.mark.asyncio
@patch(
    "jit.network.interceptor.PlaywrightResponseAdapter.from_playwright",
    new_callable=AsyncMock,
)
async def test_response_adapter_called_once(
    adapter,
):
    recorder = Mock()

    interceptor = NetworkInterceptor(recorder)

    adapter.return_value = HttpResponse(
        request_id="1",
        status=200,
    )

    response = Mock()
    response.request = Mock()

    await interceptor._handle_response(response)

    assert adapter.await_count == 1


@pytest.mark.asyncio
@patch(
    "jit.network.interceptor.PlaywrightRequestAdapter.from_playwright",
    new_callable=AsyncMock,
)
async def test_request_entity_forwarded(
    adapter,
):
    recorder = Mock()

    interceptor = NetworkInterceptor(recorder)

    entity = HttpRequest(
        url="https://abc.com",
    )

    adapter.return_value = entity

    await interceptor._handle_request(Mock())

    recorded = recorder.record_request.call_args.args[0]

    assert recorded is entity


@pytest.mark.asyncio
@patch(
    "jit.network.interceptor.PlaywrightResponseAdapter.from_playwright",
    new_callable=AsyncMock,
)
async def test_response_entity_forwarded(
    adapter,
):
    recorder = Mock()

    interceptor = NetworkInterceptor(recorder)

    entity = HttpResponse(
        request_id="xyz",
        status=200,
    )

    adapter.return_value = entity

    response = Mock()
    response.request = Mock()

    await interceptor._handle_response(response)

    recorded = recorder.record_response.call_args.args[0]

    assert recorded is entity
