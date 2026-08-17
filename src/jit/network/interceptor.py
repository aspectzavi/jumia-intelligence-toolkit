from __future__ import annotations

import asyncio

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
        self._pending_tasks: set[asyncio.Task[None]] = set()

    async def attach(
        self,
        target: Page | BrowserContext,
    ) -> None:
        """
        Attach event listeners.
        """

        target.on(
            "request",
            self._on_request,
        )

        target.on(
            "response",
            self._on_response,
        )

    def _on_request(
        self,
        request: Request,
    ) -> None:
        """
        Synchronous Playwright callback for the 'request' event.

        Schedules the async handler as a tracked task so drain() can
        await it before the browser context is torn down.
        """

        self._track(
            asyncio.create_task(
                self._handle_request(request),
            )
        )

    def _on_response(
        self,
        response: Response,
    ) -> None:
        """
        Synchronous Playwright callback for the 'response' event.
        """

        self._track(
            asyncio.create_task(
                self._handle_response(response),
            )
        )

    def _track(
        self,
        task: asyncio.Task[None],
    ) -> None:
        self._pending_tasks.add(task)
        task.add_done_callback(self._pending_tasks.discard)

    async def drain(self) -> None:
        """
        Wait for all in-flight request/response handlers to finish.

        Must be called before closing the browser context, otherwise
        in-flight header/body reads race the context teardown and
        silently fail (surfacing as missing schemas/examples or a
        TargetClosedError logged by the event loop).
        """

        while self._pending_tasks:
            pending = list(self._pending_tasks)
            await asyncio.gather(
                *pending,
                return_exceptions=True,
            )

    async def _handle_request(
        self,
        request: Request,
    ) -> None:
        """
        Handle a Playwright request.
        """

        try:
            entity = await PlaywrightRequestAdapter.from_playwright(request)
        except Exception:
            return

        self._recorder.record_request(entity)

    async def _handle_response(
        self,
        response: Response,
    ) -> None:
        """
        Handle a Playwright response.
        """

        try:
            entity = await PlaywrightResponseAdapter.from_playwright(
                response,
                request_id=str(id(response.request)),
            )
        except Exception:
            return

        self._recorder.record_response(entity)
