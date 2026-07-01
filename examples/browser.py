import asyncio

from jit.browser import BrowserManager
from jit.config.settings import settings


async def main():

    async with BrowserManager() as browser, browser.new_context() as context:
        page = await context.new_page()

        await page.goto(settings.base_url)

        await page.wait_for_timeout(5000)


if __name__ == "__main__":
    asyncio.run(main())
