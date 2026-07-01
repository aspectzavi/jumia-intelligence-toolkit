from __future__ import annotations

import json
from pathlib import Path

from playwright.async_api import BrowserContext

from jit.config.settings import settings
from jit.utils import logger


class SessionManager:
    """
    Handles Playwright storage state.
    """

    def __init__(self) -> None:
        self.state_path = Path(settings.state_path)

    @property
    def exists(self) -> bool:
        """
        Check whether the storage state file exists.
        """
        return self.state_path.exists()

    @property
    def is_valid(self) -> bool:
        """
        Validate that the storage state file:
        - exists
        - is not empty
        - contains valid JSON
        """

        if not self.exists:
            return False

        try:
            if self.state_path.stat().st_size == 0:
                logger.warning("Storage state file exists but is empty.")
                return False

            with self.state_path.open(
                "r",
                encoding="utf-8",
            ) as file:
                json.load(file)

            return True

        except json.JSONDecodeError:
            logger.warning("Storage state contains invalid JSON.")
            return False

        except Exception as exc:
            logger.warning(f"Unable to validate storage state: {exc}")
            return False

    async def save(
        self,
        context: BrowserContext,
    ) -> None:
        """
        Save browser storage state.
        """

        self.state_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        await context.storage_state(path=str(self.state_path))

        logger.info(f"Storage state saved to {self.state_path}")
