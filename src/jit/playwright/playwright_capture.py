from __future__ import annotations

from playwright.sync_api import (
    Browser,
    BrowserContext,
    Page,
    Playwright,
    sync_playwright,
)

from jit.discovery.api_mapper import ApiMapper
from jit.playwright.event_handlers import EventHandlers


class PlaywrightCapture:
    """
    Controls a Playwright browser session and connects browser
    events to the API discovery pipeline.
    """

    def __init__(self) -> None:
        self.mapper = ApiMapper()
        self.handlers = EventHandlers(self.mapper)

        self.started = False

        self._playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None

    def start(self) -> None:
        """
        Launch Chromium.
        """

        if self.started:
            return

        self._playwright = sync_playwright().start()

        self.browser = self._playwright.chromium.launch(
            headless=True,
        )

        self.context = self.browser.new_context()

        self.page = self.context.new_page()

        self.started = True

    def stop(self) -> None:
        """
        Close browser resources.
        """

        if self.page is not None:
            self.page.close()
            self.page = None

        if self.context is not None:
            self.context.close()
            self.context = None

        if self.browser is not None:
            self.browser.close()
            self.browser = None

        if self._playwright is not None:
            self._playwright.stop()
            self._playwright = None

        self.started = False

    def register_events(self) -> None:
        """
        Register Playwright network event callbacks.
        """

        assert self.page is not None

        self.page.on(
            "request",
            lambda request: self.handlers.on_request(request),
        )

        # Response registration will be added later once
        # request/response correlation is implemented.
