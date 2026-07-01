from __future__ import annotations

from types import TracebackType
from typing import TYPE_CHECKING

from playwright.async_api import (
    Browser,
    BrowserType,
    Playwright,
    async_playwright,
)

from jit.config.settings import settings
from jit.utils import logger

if TYPE_CHECKING:
    from .context import ContextManager


SUPPORTED_BROWSERS = {
    "chromium",
    "firefox",
    "webkit",
}


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

    @property
    def browser(self) -> Browser:
        """
        Return the active Playwright browser.

        Raises:
            RuntimeError: If the browser has not been started.
        """
        if self._browser is None:
            raise RuntimeError("Browser has not been started.")

        return self._browser

    async def start(self) -> Browser:
        """
        Start Playwright and launch the configured browser.
        """

        if self._browser is not None:
            logger.warning("Browser is already running.")
            return self._browser

        logger.info("Starting Playwright...")

        try:
            self._playwright = await async_playwright().start()

            if settings.browser not in SUPPORTED_BROWSERS:
                raise ValueError(
                    f"Unsupported browser '{settings.browser}'. "
                    f"Supported browsers: "
                    f"{', '.join(sorted(SUPPORTED_BROWSERS))}"
                )

            browser_type: BrowserType = getattr(
                self._playwright,
                settings.browser,
            )

            self._browser = await browser_type.launch(
                headless=settings.headless,
                slow_mo=settings.slow_mo,
            )

            logger.success(f"{settings.browser} launched successfully.")

            return self._browser

        except Exception:
            logger.exception("Failed to launch browser.")

            if self._playwright is not None:
                try:
                    await self._playwright.stop()
                except Exception:
                    logger.exception("Failed to stop Playwright during cleanup.")

            self._browser = None
            self._playwright = None

            raise

    def new_context(self) -> ContextManager:
        """
        Return a managed browser context.

        The actual BrowserContext is created when entering
        the async context manager.
        """

        if self._browser is None:
            raise RuntimeError("Browser has not been started.")

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
            logger.exception("Error while closing browser.")

        try:
            if self._playwright is not None:
                await self._playwright.stop()

        except Exception:
            logger.exception("Error while stopping Playwright.")

        finally:
            self._browser = None
            self._playwright = None

        logger.success("Browser closed.")

    async def __aenter__(self) -> BrowserManager:
        """
        Enter the async context manager.
        """

        await self.start()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        """
        Exit the async context manager.
        """

        await self.stop()
