from pathlib import Path

from playwright.async_api import BrowserContext

from jit.config.settings import settings


async def save_storage_state(context: BrowserContext) -> None:
    """
    Save Playwright storage state.
    """

    Path(settings.state_path).parent.mkdir(parents=True, exist_ok=True)

    await context.storage_state(path=settings.state_path)


async def has_storage_state() -> bool:
    """
    Check whether a storage state file exists.
    """

    return Path(settings.state_path).exists()
