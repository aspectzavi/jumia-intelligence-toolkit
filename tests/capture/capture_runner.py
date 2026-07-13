from __future__ import annotations

from playwright.async_api import Page

from jit.browser.browser import BrowserManager
from jit.network.capture import CaptureSession


class CaptureRunner:
    """
    Runs a complete browser capture session.

    Responsibilities
    ----------------
    - Launch a browser
    - Create a browser context
    - Open a page
    - Attach network capture
    - Navigate to a URL
    - Wait for network activity to finish
    - Return the populated CaptureSession
    """

    async def capture(
        self,
        url: str,
    ) -> CaptureSession:
        """
        Capture all network traffic generated while loading a page.

        Parameters
        ----------
        url:
            URL to visit.

        Returns
        -------
        CaptureSession
            Contains all captured requests, responses,
            and discovered endpoints.
        """

        async with BrowserManager() as browser:

            async with browser.new_context() as context:

                page: Page = await context.new_page()

                await page.goto(
                    url,
                    wait_until="networkidle",
                )

                #
                # Ensure endpoint detector is populated
                #
                context.capture.process()

                return context.capture
