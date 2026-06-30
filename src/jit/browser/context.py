from pathlib import Path

from playwright.async_api import Browser, BrowserContext, Page

from jit.browser.session import SessionManager
from jit.config.settings import settings
from jit.utils import logger


class ContextManager:
    """
    Manages a Playwright BrowserContext.
    """

    def __init__(self, browser: Browser):
        self.browser = browser
        self.context: BrowserContext | None = None
        self.session = SessionManager()

    async def start(self) -> BrowserContext:

        logger.info("Creating browser context...")

        kwargs = {
            "viewport": {
                "width": settings.viewport_width,
                "height": settings.viewport_height,
            },
            "locale": settings.locale,
            "timezone_id": settings.timezone,
            "accept_downloads": True,
        }

        if settings.user_agent:
            kwargs["user_agent"] = settings.user_agent

        if self.session.is_valid:
            logger.info("Loading storage state...")
            kwargs["storage_state"] = str(self.session.state_path)
        else:
            logger.info(
                "No valid storage state found. Starting a fresh browser context."
            )

        Path(settings.download_path).mkdir(
            parents=True,
            exist_ok=True,
        )

        try:
            self.context = await self.browser.new_context(**kwargs)

            logger.success("Context created.")

            return self.context

        except Exception:
            logger.exception(
                "Failed to create browser context."
            )
            raise

    async def new_page(self) -> Page:
        if self.context is None:
            raise RuntimeError(
                "Context has not been started."
            )

        return await self.context.new_page()

    async def stop(self) -> None:

        if self.context is None:
            return

        try:
            logger.info("Saving browser state...")

            await self.session.save(self.context)

        except Exception:
            logger.exception(
                "Failed to save storage state."
            )

        try:
            logger.info("Closing context...")

            await self.context.close()

        except Exception:
            logger.exception(
                "Failed to close browser context."
            )

        logger.success("Context closed.")

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.stop()
