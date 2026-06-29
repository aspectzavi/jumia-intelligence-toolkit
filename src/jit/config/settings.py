from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Global application configuration.

    Values are loaded from the .env file and environment variables.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Browser
    browser: str = Field(default="chromium")
    headless: bool = Field(default=True)
    slow_mo: int = Field(default=200)
    timeout: int = Field(default=30000)

    # Website
    base_url: str = Field(default="https://www.jumia.co.ke")

    # Locale
    locale: str = Field(default="en-KE")
    timezone: str = Field(default="Africa/Nairobi")

    # Viewport
    viewport_width: int = Field(default=1920)
    viewport_height: int = Field(default=1080)

    # User Agent
    user_agent: str = Field(default="")

    # Logging
    log_level: str = Field(default="INFO")
    log_file: str = Field(default="logs/jit.log")
    log_rotation: str = Field(default="10 MB")
    log_retention: str = Field(default="30 days")

    # Storage
    state_path: str = Field(default="data/playwright/storage_state.json")
    cookie_path: str = Field(default="data/playwright/cookies.json")
    download_path: str = Field(default="data/playwright/downloads")
    trace_path: str = Field(default="data/playwright/traces")

    # Captures
    capture_path: str = Field(default="data/captures")
    request_path: str = Field(default="data/captures/requests")
    response_path: str = Field(default="data/captures/responses")
    screenshot_path: str = Field(default="data/captures/screenshots")
    video_path: str = Field(default="data/captures/videos")


@lru_cache
def get_settings() -> Settings:
    """
    Return a cached Settings instance.
    """
    return Settings()


settings = get_settings()
