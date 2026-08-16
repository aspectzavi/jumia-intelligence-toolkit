from __future__ import annotations

from collections.abc import Iterator

from jit.analyzer.endpoint_analyzer import EndpointAnalyzer
from jit.capture.capture_runner import CaptureRunner
from jit.discovery.api_mapper import ApiMapper
from jit.entities.api_endpoint import ApiEndpoint
from jit.entities.http_request import HttpRequest
from jit.openapi.openapi_document import OpenApiDocument
from jit.openapi.openapi_generator import OpenApiGenerator


class DiscoveryPipeline:
    """
    High-level orchestration for API discovery.

    Pipeline
    --------
        CaptureRunner
            ↓
        CaptureSession
            ↓
        ApiMapper
            ↓
        EndpointAnalyzer
            ↓
        OpenApiGenerator
    """

    def __init__(self) -> None:
        self._mapper = ApiMapper()
        self._analyzer = EndpointAnalyzer()
        self._last_request_count = 0
        self._last_response_count = 0
        self._last_requests: list[HttpRequest] = []

    @property
    def mapper(self) -> ApiMapper:
        """
        Return the underlying API mapper.
        """
        return self._mapper

    @property
    def last_request_count(self) -> int:
        """
        Number of requests captured during the most recent discover() call.
        """
        return self._last_request_count

    @property
    def last_response_count(self) -> int:
        """
        Number of responses captured during the most recent discover() call.
        """
        return self._last_response_count

    @property
    def last_requests(self) -> list[HttpRequest]:
        """
        Raw requests captured during the most recent discover() call.

        Useful for traffic classification/reporting without duplicating
        capture responsibilities already owned by CaptureSession.
        """
        return self._last_requests

    @property
    def endpoints(self) -> list[ApiEndpoint]:
        """
        Return all discovered endpoints.
        """
        return self._mapper.endpoints

    async def discover(
        self,
        url: str,
    ) -> list[ApiEndpoint]:
        """
        Capture network traffic and discover API endpoints.
        """

        runner = CaptureRunner()

        session = await runner.capture(url)

        self._last_request_count = session.request_count
        self._last_response_count = session.response_count
        self._last_requests = list(session.requests)

        #
        # Feed captured traffic into the mapper.
        #
        for request in session.requests:
            self._mapper.add_request(request)

        for response in session.responses:
            self._mapper.add_response(response)

        #
        # Enrich every endpoint.
        #
        for endpoint in self._mapper:
            self._analyzer.analyze(endpoint)

        return self._mapper.endpoints

    async def discover_openapi(
        self,
        url: str,
        *,
        title: str = "Discovered API",
        version: str = "1.0.0",
    ) -> OpenApiDocument:
        """
        Capture a website and immediately build an OpenAPI document.
        """

        await self.discover(url)

        return OpenApiGenerator.generate(
            self._mapper,
            title=title,
            version=version,
        )

    def clear(self) -> None:
        """
        Reset the pipeline.
        """
        self._mapper.clear()

    def __len__(self) -> int:
        return len(self._mapper)

    def __iter__(self) -> Iterator[ApiEndpoint]:
        return iter(self._mapper)

    def __str__(self) -> str:
        return (
            f"DiscoveryPipeline("
            f"{len(self)} endpoints)"
        )
