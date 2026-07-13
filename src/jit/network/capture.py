from __future__ import annotations

from playwright.async_api import BrowserContext, Page

from jit.discovery.endpoint_detector import EndpointDetector
from jit.entities.api_endpoint import ApiEndpoint
from jit.entities.http_request import HttpRequest
from jit.entities.http_response import HttpResponse
from jit.network.interceptor import NetworkInterceptor
from jit.network.recorder import NetworkRecorder


class CaptureSession:
    """
    Coordinates network capture for a browser session.

    Responsibilities
    ----------------
    - Attach the NetworkInterceptor to a Page or BrowserContext
    - Record requests and responses
    - Build API endpoints
    - Expose captured traffic through a clean interface

    Higher-level processing (schema inference, API mapping,
    OpenAPI generation, etc.) can be added later without
    changing this public API.
    """

    def __init__(self) -> None:
        self._recorder = NetworkRecorder()
        self._detector = EndpointDetector()
        self._interceptor = NetworkInterceptor(
            self._recorder,
        )

    async def attach(
        self,
        target: Page | BrowserContext,
    ) -> None:
        """
        Attach the capture session to a Playwright target.
        """

        await self._interceptor.attach(target)

    def process(self) -> None:
        """
        Process all captured traffic.

        Groups requests and responses into API endpoints.
        Safe to call multiple times.
        """

        self._detector.clear()

        #
        # Build endpoints from requests.
        #
        for request in self._recorder.requests:
            self._detector.add_request(request)

        #
        # Attach responses.
        #
        for response in self._recorder.responses:
            self._detector.add_response(response)

    @property
    def requests(self) -> list[HttpRequest]:
        """
        Captured HTTP requests.
        """

        return self._recorder.requests

    @property
    def responses(self) -> list[HttpResponse]:
        """
        Captured HTTP responses.
        """

        return self._recorder.responses

    @property
    def endpoints(self) -> list[ApiEndpoint]:
        """
        Discovered API endpoints.

        Automatically processes pending traffic.
        """

        self.process()
        return self._detector.all()

    @property
    def recorder(self) -> NetworkRecorder:
        """
        Underlying recorder.
        """

        return self._recorder

    @property
    def detector(self) -> EndpointDetector:
        """
        Endpoint detector.
        """

        return self._detector

    @property
    def request_count(self) -> int:
        """
        Number of captured requests.
        """

        return self._recorder.request_count

    @property
    def response_count(self) -> int:
        """
        Number of captured responses.
        """

        return self._recorder.response_count

    @property
    def endpoint_count(self) -> int:
        """
        Number of discovered endpoints.
        """

        self.process()
        return len(self._detector)

    def clear(self) -> None:
        """
        Reset the capture session.
        """

        self._recorder.clear()
        self._detector.clear()
