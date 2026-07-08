from __future__ import annotations

from typing import Any

from jit.entities.http_cookie import HttpCookie


class HttpCookieSerializer:
    """
    Serializer for HttpCookie entities.
    """

    @staticmethod
    def to_dict(
        cookie: HttpCookie,
    ) -> dict[str, Any]:
        return {
            "name": cookie.name,
            "value": cookie.value,
            "domain": cookie.domain,
            "path": cookie.path,
            "expires": cookie.expires,
            "secure": cookie.secure,
            "http_only": cookie.http_only,
            "same_site": cookie.same_site,
        }

    @staticmethod
    def from_dict(
        data: dict[str, Any],
    ) -> HttpCookie:
        return HttpCookie(
            name=data["name"],
            value=data["value"],
            domain=data.get("domain"),
            path=data.get("path", "/"),
            expires=data.get("expires"),
            secure=data.get("secure", False),
            http_only=data.get("http_only", False),
            same_site=data.get("same_site"),
        )
