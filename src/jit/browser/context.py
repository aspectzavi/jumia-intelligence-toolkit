from __future__ import annotations

from pathlib import Path
from types import TracebackType

from playwright.async_api import Browser, BrowserContext, Page

from jit.browser.session import SessionManager
from jit.config.settings import settings
from jit.utils import logger


class ContextManager:
    """
    Manages a Playwright BrowserContext.

    Responsibilities:
    - Create browser contexts
    - Restore browser session state
    - Save browser session state
    - Create pages
    - Clean up resources
    """

    def __init__(self, browser: Browser) -> None:
        self._browser = browser
        self._context: BrowserContext | None = None
        self._session = SessionManager()

    @property
    def context(self) -> BrowserContext:
        """
        Return the active BrowserContext.
        """

        if self._context is None:
            raise RuntimeError("Context has not been started.")

        return self._context

    async def start(self) -> BrowserContext:
        """
        Create a new browser context.
        """

        if self._context is not None:
            logger.warning("Context is already running.")
            return self._context

        logger.info("Creating browser context...")

        Path(settings.download_path).mkdir(
            parents=True,
            exist_ok=True,
        )

        storage_state: str | None = None

        if self._session.is_valid:
            logger.info("Loading storage state...")

            storage_state = str(self._session.state_path)
        else:
            logger.info("No valid storage state found. Starting a fresh browser context.")

        try:
            self._context = await self._browser.new_context(
                viewport={
                    "width": settings.viewport_width,
                    "height": settings.viewport_height,
                },
                locale=settings.locale,
                timezone_id=settings.timezone,
                user_agent=settings.user_agent or None,
                accept_downloads=True,
                storage_state=storage_state,
            )

            logger.success("Context created.")

            return self._context

        except Exception:
            logger.exception("Failed to create browser context.")
            raise

    async def new_page(self) -> Page:
        """
        Create a new page.
        """

        return await self.context.new_page()

    async def stop(self) -> None:
        """
        Save session state and close the browser context.
        """

        if self._context is None:
            return

        try:
            logger.info("Saving browser state...")

            await self._session.save(self._context)

        except Exception:
            logger.exception("Failed to save storage state.")

        try:
            logger.info("Closing context...")

            await self._context.close()

        except Exception:
            logger.exception("Failed to close browser context.")

        finally:
            self._context = None

        logger.success("Context closed.")

    async def __aenter__(self) -> ContextManager:
        await self.start()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        await self.stop()
