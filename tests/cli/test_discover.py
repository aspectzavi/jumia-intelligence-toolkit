from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from jit.cli.discover import run_discover
from jit.discovery.discovery_pipeline import DiscoveryPipeline
from jit.entities.header_collection import HeaderCollection
from jit.entities.http_header import HttpHeader
from jit.entities.http_request import HttpRequest


def make_request() -> HttpRequest:
    headers = HeaderCollection()
    headers.add(HttpHeader("Accept", "application/json"))

    return HttpRequest(
        id="req-1",
        method="GET",
        url="https://www.jumia.co.ke/api/products",
        resource_type="fetch",
        headers=headers,
    )


async def _fake_discover(self: DiscoveryPipeline, url: str) -> list:
    self._last_request_count = 1
    self._last_response_count = 1
    self._last_requests = [make_request()]
    self.mapper.add_request(make_request())
    return self.mapper.endpoints


@pytest.mark.asyncio
async def test_run_discover_prints_summary_and_succeeds() -> None:
    with patch.object(
        DiscoveryPipeline,
        "discover",
        new=_fake_discover,
    ):
        exit_code = await run_discover(
            "https://www.jumia.co.ke",
            export_path=None,
            title="Discovered API",
            version="1.0.0",
        )

    assert exit_code == 0


@pytest.mark.asyncio
async def test_run_discover_exports_openapi(tmp_path: Path) -> None:
    export_path = tmp_path / "openapi.yaml"

    with patch.object(
        DiscoveryPipeline,
        "discover",
        new=_fake_discover,
    ):
        exit_code = await run_discover(
            "https://www.jumia.co.ke",
            export_path=str(export_path),
            title="Discovered API",
            version="1.0.0",
        )

    assert exit_code == 0
    assert export_path.exists()


@pytest.mark.asyncio
async def test_run_discover_returns_nonzero_on_failure() -> None:
    async def _failing_discover(self: DiscoveryPipeline, url: str) -> list:
        raise RuntimeError("navigation timeout")

    with patch.object(
        DiscoveryPipeline,
        "discover",
        new=_failing_discover,
    ):
        exit_code = await run_discover(
            "https://www.jumia.co.ke",
            export_path=None,
            title="Discovered API",
            version="1.0.0",
        )

    assert exit_code == 1
