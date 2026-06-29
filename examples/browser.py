import asyncio

from jit.browser import BrowserManager
from jit.browser.context import create_context
from jit.config.settings import settings


async def main():
    async with BrowserManager() as manager:
        context = await create_context(manager.browser)

        page = await context.new_page()

        await page.goto(settings.base_url)

        await page.wait_for_timeout(50000)

        await context.close()


if __name__ == "__main__":
    asyncio.run(main())
