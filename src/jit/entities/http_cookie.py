from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True, frozen=True)
class HttpCookie:
    """
    Represents a single HTTP cookie.

    This entity is provider-agnostic and can be used with
    Playwright, Requests, Selenium, or exported to JSON.
    """

    name: str
    value: str

    domain: str
    path: str = "/"

    expires: float | None = None

    secure: bool = False
    http_only: bool = False

    same_site: str | None = None

    def is_expired(self, current_time: float) -> bool:
        """
        Determine whether the cookie has expired.

        Args:
            current_time:
                Current Unix timestamp.

        Returns:
            True if expired.
        """

        if self.expires is None:
            return False

        return current_time >= self.expires

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize the cookie.
        """

        return {
            "name": self.name,
            "value": self.value,
            "domain": self.domain,
            "path": self.path,
            "expires": self.expires,
            "secure": self.secure,
            "http_only": self.http_only,
            "same_site": self.same_site,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> HttpCookie:
        """
        Create a cookie from a dictionary.
        """

        return cls(
            name=data["name"],
            value=data["value"],
            domain=data["domain"],
            path=data.get("path", "/"),
            expires=data.get("expires"),
            secure=data.get("secure", False),
            http_only=data.get("http_only", False),
            same_site=data.get("same_site"),
        )

    def __str__(self) -> str:
        return (
            f"{self.name}={self.value}; "
            f"Domain={self.domain}; "
            f"Path={self.path}"
        )
