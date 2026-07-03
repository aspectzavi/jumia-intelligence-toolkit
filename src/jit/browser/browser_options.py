from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class BrowserOptions:
    """
    Configuration for browser sessions and network capture.
    """

    headless: bool = True

    timeout: int = 30000

    record_requests: bool = True

    record_responses: bool = True

    record_images: bool = False

    record_fonts: bool = False

    record_stylesheets: bool = False

    record_scripts: bool = True

    user_agent: str | None = None

    viewport_width: int = 1280

    viewport_height: int = 720
