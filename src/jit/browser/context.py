from playwright.async_api import BrowserContext

from jit.config.settings import settings


async def create_context(browser):
    """
    Create a configured browser context.
    """

    context: BrowserContext = await browser.new_context(
        viewport={
            "width": settings.viewport_width,
            "height": settings.viewport_height,
        },
        locale=settings.locale,
        timezone_id=settings.timezone,
        accept_downloads=True,
    )

    return context
