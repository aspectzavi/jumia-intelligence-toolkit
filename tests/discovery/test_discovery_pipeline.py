from __future__ import annotations

import json
from unittest.mock import AsyncMock, patch

import pytest

from jit.discovery.discovery_pipeline import DiscoveryPipeline
from jit.entities.header_collection import HeaderCollection
from jit.entities.http_header import HttpHeader
from jit.entities.http_request import HttpRequest
from jit.entities.http_response import HttpResponse
from jit.network.capture import CaptureSession


def make_session(
    *,
    with_response: bool = True,
) -> CaptureSession:
    """
    Build a populated CaptureSession without touching a real browser.
    """

    session = CaptureSession()

    request = HttpRequest(
        id="req-1",
        method="GET",
        url="https://www.jumia.co.ke/api/products?page=1",
        resource_type="fetch",
    )

    session.recorder.requests.append(request)

    if with_response:
        headers = HeaderCollection()
        headers.add(HttpHeader("Content-Type", "application/json"))

        response = HttpResponse(
            request_id="req-1",
            status=200,
            headers=headers,
            body=json.dumps({"id": 1, "name": "Phone"}).encode("utf-8"),
        )

        session.recorder.responses.append(response)

    session.process()

    return session


@pytest.mark.asyncio
async def test_discover_maps_and_analyzes_captured_traffic():
    pipeline = DiscoveryPipeline()

    with patch(
        "jit.discovery.discovery_pipeline.CaptureRunner.capture",
        new=AsyncMock(return_value=make_session()),
    ):
        endpoints = await pipeline.discover(
            "https://www.jumia.co.ke",
        )

    assert len(endpoints) == 1

    endpoint = endpoints[0]
    assert endpoint.method == "GET"
    assert endpoint.request_count == 1
    assert endpoint.response_count == 1
    assert endpoint.response_schema is not None
    assert endpoint.confidence == 0.35
    assert endpoint.status_codes == {200: 1}



@pytest.mark.asyncio
async def test_discover_handles_requests_without_responses():
    pipeline = DiscoveryPipeline()

    with patch(
        "jit.discovery.discovery_pipeline.CaptureRunner.capture",
        new=AsyncMock(return_value=make_session(with_response=False)),
    ):
        endpoints = await pipeline.discover(
            "https://www.jumia.co.ke",
        )

    assert len(endpoints) == 1
    assert endpoints[0].response_count == 0
    assert endpoints[0].confidence == 0.0


@pytest.mark.asyncio
async def test_discover_openapi_returns_document_with_discovered_paths():
    pipeline = DiscoveryPipeline()

    with patch(
        "jit.discovery.discovery_pipeline.CaptureRunner.capture",
        new=AsyncMock(return_value=make_session()),
    ):
        document = await pipeline.discover_openapi(
            "https://www.jumia.co.ke",
            title="Jumia API",
            version="0.1.0",
        )

    assert document.title == "Jumia API"
    assert document.version == "0.1.0"
    assert document.get_path("/api/products") is not None


@pytest.mark.asyncio
async def test_discover_is_idempotent_across_calls():
    pipeline = DiscoveryPipeline()

    with patch(
        "jit.discovery.discovery_pipeline.CaptureRunner.capture",
        new=AsyncMock(return_value=make_session()),
    ):
        await pipeline.discover("https://www.jumia.co.ke")
        await pipeline.discover("https://www.jumia.co.ke")

    # Same endpoint captured twice accumulates onto one endpoint,
    # it does not duplicate entries in the mapper.
    assert len(pipeline) == 1
    assert pipeline.endpoints[0].request_count == 2


def test_clear_resets_pipeline():
    pipeline = DiscoveryPipeline()
    pipeline.mapper.add_request(
        HttpRequest(
            id="req-1",
            method="GET",
            url="https://www.jumia.co.ke/api/products",
        )
    )

    assert len(pipeline) == 1

    pipeline.clear()

    assert len(pipeline) == 0
