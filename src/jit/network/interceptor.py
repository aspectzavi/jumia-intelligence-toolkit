from __future__ import annotations

from playwright.async_api import BrowserContext, Page, Request, Response

from jit.adapters.playwright_request_adapter import (
    PlaywrightRequestAdapter,
)
from jit.adapters.playwright_response_adapter import (
    PlaywrightResponseAdapter,
)
from jit.network.recorder import NetworkRecorder


class NetworkInterceptor:
    """
    Captures browser network traffic and forwards it
    to a NetworkRecorder.
    """

    def __init__(
        self,
        recorder: NetworkRecorder,
    ) -> None:
        self._recorder = recorder

    async def attach(
        self,
        target: Page | BrowserContext,
    ) -> None:
        """
        Attach event listeners.
        """

        target.on(
            "request",
            self._handle_request,
        )

        target.on(
            "response",
            self._handle_response,
        )

    async def _handle_request(
        self,
        request: Request,
    ) -> None:
        """
        Handle a Playwright request.
        """

        entity = await PlaywrightRequestAdapter.from_playwright(request)

        self._recorder.record_request(entity)

    async def _handle_response(
        self,
        response: Response,
    ) -> None:
        """
        Handle a Playwright response.
        """

        entity = await PlaywrightResponseAdapter.from_playwright(
            response,
            request_id=str(id(response.request)),
        )

        self._recorder.record_response(entity)
