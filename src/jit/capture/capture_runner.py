from __future__ import annotations

from typing import Literal

from jit.browser.browser import BrowserManager
from jit.network.capture import CaptureSession

WaitUntil = Literal[
    "commit",
    "domcontentloaded",
    "load",
    "networkidle",
]


class CaptureRunner:
    """
    High-level network capture runner.

    Example
    -------
    runner = CaptureRunner()

    capture = await runner.capture(
        "https://www.jumia.co.ke/",
    )

    print(capture.endpoint_count)
    """

    async def capture(
        self,
        url: str,
        *,
        wait_until: WaitUntil = "networkidle",
    ) -> CaptureSession:
        """
        Launch a browser, capture all network traffic for a page,
        then return the populated CaptureSession.
        """

        async with BrowserManager() as browser:
            async with browser.new_context() as context:

                capture = CaptureSession()

                await capture.attach(context.context)

                page = await context.new_page()

                await page.goto(
                    url,
                    wait_until=wait_until,
                )

                # Ensure endpoints are built before returning.
                capture.process()

                return capture
