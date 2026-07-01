from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from jit.entities.http_cookie import HttpCookie


class CookieAdapter:
    """
    Converts between various cookie representations and
    HttpCookie entities.

    This adapter has no dependency on Playwright.
    """

    @staticmethod
    def empty() -> list[HttpCookie]:
        """
        Create an empty cookie list.
        """
        return []

    @staticmethod
    def from_mapping(
        cookies: Mapping[str, str] | None,
    ) -> list[HttpCookie]:
        """
        Convert a simple cookie mapping into HttpCookie objects.

        Example:
            {
                "session": "...",
                "token": "...",
            }
        """

        if not cookies:
            return []

        return [
            HttpCookie(
                name=name,
                value=value,
            )
            for name, value in cookies.items()
        ]

    @staticmethod
    def from_list(
        cookies: list[dict[str, Any]] | None,
    ) -> list[HttpCookie]:
        """
        Convert browser cookie dictionaries into HttpCookie objects.
        """

        if not cookies:
            return []

        result: list[HttpCookie] = []

        for cookie in cookies:
            result.append(
                HttpCookie(
                    name=cookie["name"],
                    value=cookie["value"],
                    domain=cookie.get("domain"),
                    path=cookie.get("path", "/"),
                    expires=cookie.get("expires"),
                    secure=cookie.get("secure", False),
                    http_only=cookie.get("httpOnly", False),
                    same_site=cookie.get("sameSite"),
                )
            )

        return result

    @staticmethod
    def to_mapping(
        cookies: list[HttpCookie],
    ) -> dict[str, str]:
        """
        Convert cookies into a simple mapping.
        """

        return {cookie.name: cookie.value for cookie in cookies}

    @staticmethod
    def clone(
        cookies: list[HttpCookie],
    ) -> list[HttpCookie]:
        """
        Create a deep copy of cookies.
        """

        return [HttpCookie.from_dict(cookie.to_dict()) for cookie in cookies]

    @staticmethod
    def serialize(
        cookies: list[HttpCookie],
    ) -> list[dict[str, Any]]:
        """
        Serialize cookies.
        """

        return [cookie.to_dict() for cookie in cookies]

    @staticmethod
    def deserialize(
        data: list[dict[str, Any]],
    ) -> list[HttpCookie]:
        """
        Deserialize cookies.
        """

        return [HttpCookie.from_dict(item) for item in data]

    @staticmethod
    def from_cookie_header(
        header: str | None,
    ) -> list[HttpCookie]:
        """
        Parse a Cookie request header.
        """

        if not header:
            return []

        cookies: list[HttpCookie] = []

        for part in header.split(";"):
            part = part.strip()

            if "=" not in part:
                continue

            name, value = part.split("=", 1)

            cookies.append(
                HttpCookie(
                    name=name.strip(),
                    value=value.strip(),
                    domain=None,
                )
            )

        return cookies
