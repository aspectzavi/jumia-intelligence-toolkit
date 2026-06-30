from __future__ import annotations

from playwright.async_api import (
    Browser,
    BrowserType,
    Playwright,
    async_playwright,
)

from jit.config.settings import settings
from jit.utils import logger


class BrowserManager:
    """
    Manages the Playwright lifecycle.

    Responsibilities:
    - Start Playwright
    - Launch the configured browser
    - Create managed browser contexts
    - Shutdown the browser cleanly
    """

    def __init__(self) -> None:
        self._playwright: Playwright | None = None
        self._browser: Browser | None = None

    async def start(self) -> Browser:
        """
        Start Playwright and launch the configured browser.
        """

        logger.info("Starting Playwright...")

        try:
            self._playwright = await async_playwright().start()

            browser_type: BrowserType = getattr(
                self._playwright,
                settings.browser,
            )

            self._browser = await browser_type.launch(
                headless=settings.headless,
                slow_mo=settings.slow_mo,
            )

            logger.success(
                f"{settings.browser} launched successfully."
            )

            return self._browser

        except Exception:
            logger.exception(
                "Failed to launch browser."
            )

            if self._playwright is not None:
                await self._playwright.stop()

            raise

    def new_context(self):
        """
        Return a ContextManager.

        The browser context itself is created when entering the
        async context manager.
        """

        if self._browser is None:
            raise RuntimeError(
                "Browser has not been started."
            )

        # Local import avoids circular imports
        from .context import ContextManager

        return ContextManager(self._browser)

    async def stop(self) -> None:
        """
        Close the browser and stop Playwright.
        """

        logger.info("Closing browser...")

        try:
            if self._browser is not None:
                await self._browser.close()

        except Exception:
            logger.exception(
                "Error while closing browser."
            )

        try:
            if self._playwright is not None:
                await self._playwright.stop()

        except Exception:
            logger.exception(
                "Error while stopping Playwright."
            )

        logger.success("Browser closed.")

    async def __aenter__(self) -> BrowserManager:
        await self.start()
        return self

    async def __aexit__(
        self,
        exc_type,
        exc_val,
        exc_tb,
    ) -> None:
        await self.stop()
