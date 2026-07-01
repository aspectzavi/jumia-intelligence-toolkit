from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from urllib.parse import ParseResult, parse_qs, urlparse
from uuid import uuid4

from jit.entities.header_collection import HeaderCollection
from jit.entities.http_cookie import HttpCookie
from jit.entities.http_header import HttpHeader
from jit.entities.request_timing import RequestTiming


@dataclass(slots=True)
class HttpRequest:
    """
    Represents a captured HTTP request.

    This entity is transport-layer only and is independent of
    Playwright, Requests, Selenium, or any other HTTP library.
    """

    id: str = field(default_factory=lambda: str(uuid4()))

    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))

    url: str = ""

    method: str = "GET"

    resource_type: str = "other"

    frame_url: str | None = None

    is_navigation: bool = False

    post_data: str | None = None

    headers: HeaderCollection = field(default_factory=HeaderCollection)

    cookies: list[HttpCookie] = field(default_factory=list)

    timing: RequestTiming = field(default_factory=RequestTiming.start_now)

    @property
    def parsed_url(self) -> ParseResult:
        """
        Parsed URL object.
        """
        return urlparse(self.url)

    @property
    def hostname(self) -> str:
        """
        Request hostname.
        """
        return self.parsed_url.netloc

    @property
    def path(self) -> str:
        """
        URL path.
        """
        return self.parsed_url.path

    @property
    def scheme(self) -> str:
        """
        URL scheme.
        """
        return self.parsed_url.scheme

    @property
    def query_parameters(self) -> dict[str, list[str]]:
        """
        Parsed query parameters.
        """
        return parse_qs(
            self.parsed_url.query,
            keep_blank_values=True,
        )

    @property
    def header_map(self) -> dict[str, str]:
        """
        Headers as a case-insensitive dictionary.
        """
        return self.headers.as_dict

    @property
    def cookie_map(self) -> dict[str, str]:
        """
        Cookies as a dictionary.
        """
        return {cookie.name: cookie.value for cookie in self.cookies}

    @property
    def content_type(self) -> str | None:
        """
        Content-Type header.
        """
        return self.headers.content_type

    @property
    def is_json(self) -> bool:
        """
        Whether this request contains JSON.
        """
        content_type = self.content_type

        if content_type is None:
            return False

        return "application/json" in content_type.lower()

    @property
    def is_post(self) -> bool:
        return self.method.upper() == "POST"

    @property
    def is_get(self) -> bool:
        return self.method.upper() == "GET"

    @property
    def is_api(self) -> bool:
        """
        Heuristic indicating whether this appears to be an API call.
        """

        path = self.path.lower()

        return any(
            keyword in path
            for keyword in (
                "/api/",
                "/graphql",
                "/rest/",
                "/ajax/",
                "/v1/",
                "/v2/",
            )
        )

    def add_header(
        self,
        header: HttpHeader,
    ) -> None:
        """
        Add a header.
        """
        self.headers.add(header)

    def add_cookie(
        self,
        cookie: HttpCookie,
    ) -> None:
        """
        Add a cookie.
        """
        self.cookies.append(cookie)

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize the request.
        """

        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "url": self.url,
            "method": self.method,
            "resource_type": self.resource_type,
            "frame_url": self.frame_url,
            "is_navigation": self.is_navigation,
            "post_data": self.post_data,
            "headers": self.headers.to_dict(),
            "cookies": [cookie.to_dict() for cookie in self.cookies],
            "timing": self.timing.to_dict(),
        }

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> HttpRequest:
        """
        Deserialize a request.
        """

        request = cls(
            id=data["id"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            url=data["url"],
            method=data["method"],
            resource_type=data.get(
                "resource_type",
                "other",
            ),
            frame_url=data.get("frame_url"),
            is_navigation=data.get(
                "is_navigation",
                False,
            ),
            post_data=data.get("post_data"),
            timing=RequestTiming.from_dict(data["timing"]),
        )

        request.headers = HeaderCollection.from_dict(data.get("headers", []))

        request.cookies.extend(
            HttpCookie.from_dict(item)
            for item in data.get(
                "cookies",
                [],
            )
        )

        return request

    def __str__(self) -> str:
        return f"{self.method} {self.url}"
