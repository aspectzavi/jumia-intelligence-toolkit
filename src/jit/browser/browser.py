from pathlib import Path

from playwright.async_api import Browser, BrowserType, Playwright, async_playwright

from jit.config.settings import settings
from jit.utils import logger


class BrowserManager:
    """
    Manages the Playwright lifecycle.
    """

    def __init__(self) -> None:
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None

    async def start(self) -> Browser:
        """
        Start Playwright and launch the configured browser.
        """

        logger.info("Starting Playwright...")

        self.playwright = await async_playwright().start()

        browser_type: BrowserType = getattr(self.playwright, settings.browser)

        self.browser = await browser_type.launch(
            headless=settings.headless,
            slow_mo=settings.slow_mo,
        )

        logger.success(f"{settings.browser} launched successfully.")

        return self.browser

    async def stop(self) -> None:
        """
        Shut down the browser and Playwright.
        """

        logger.info("Closing browser...")

        if self.browser:
            await self.browser.close()

        if self.playwright:
            await self.playwright.stop()

        logger.success("Browser closed.")

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.stop()
