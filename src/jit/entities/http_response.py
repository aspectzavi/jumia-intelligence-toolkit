from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, cast

from jit.entities.header_collection import HeaderCollection
from jit.entities.http_header import HttpHeader
from jit.entities.request_timing import RequestTiming


@dataclass(slots=True)
class HttpResponse:
    """
    Represents a captured HTTP response.

    This entity is transport-layer only and independent of
    Playwright or any HTTP client implementation.
    """

    request_id: str

    status: int

    status_text: str = ""

    url: str = ""

    mime_type: str | None = None

    encoding: str | None = None

    content_length: int | None = None

    body: Any = None

    redirected: bool = False

    server_ip: str | None = None

    headers: HeaderCollection = field(default_factory=HeaderCollection)

    timing: RequestTiming | None = None

    @property
    def is_success(self) -> bool:
        """
        Returns True if the response was successful.
        """
        return 200 <= self.status < 300

    @property
    def is_redirect(self) -> bool:
        """
        Returns True if the response is a redirect.
        """
        return 300 <= self.status < 400

    @property
    def is_client_error(self) -> bool:
        """
        Returns True if this is a 4xx response.
        """
        return 400 <= self.status < 500

    @property
    def is_server_error(self) -> bool:
        """
        Returns True if this is a 5xx response.
        """
        return self.status >= 500

    @property
    def header_map(self) -> dict[str, str]:
        """
        Return headers as a case-insensitive dictionary.
        """
        return {header.name.lower(): header.value for header in self.headers}

    @property
    def content_type(self) -> str | None:
        """
        Return the Content-Type header.
        """
        return self.header_map.get("content-type")

    @property
    def is_json(self) -> bool:
        """
        Whether the response contains JSON.
        """
        content_type = self.content_type

        if content_type is None:
            return False

        return "application/json" in content_type.lower()

    @property
    def is_html(self) -> bool:
        """
        Whether the response contains HTML.
        """
        content_type = self.content_type

        if content_type is None:
            return False

        return "text/html" in content_type.lower()

    @property
    def is_image(self) -> bool:
        """
        Whether the response is an image.
        """
        content_type = self.content_type

        if content_type is None:
            return False

        return content_type.lower().startswith("image/")

    @property
    def body_size(self) -> int:
        """
        Size of the response body in bytes.
        """

        if self.body is None:
            return 0

        if isinstance(self.body, bytes):
            return len(self.body)

        return len(cast(str, self.body).encode("utf-8"))

    def add_header(
        self,
        header: HttpHeader,
    ) -> None:
        """
        Add a response header.
        """
        self.headers.add(header)

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize the response.
        """

        return {
            "request_id": self.request_id,
            "status": self.status,
            "status_text": self.status_text,
            "url": self.url,
            "mime_type": self.mime_type,
            "encoding": self.encoding,
            "content_length": self.content_length,
            "body": (
                self.body.decode(
                    "utf-8",
                    errors="replace",
                )
                if isinstance(self.body, bytes)
                else self.body
            ),
            "redirected": self.redirected,
            "server_ip": self.server_ip,
            "headers": [header.to_dict() for header in self.headers],
            "timing": (self.timing.to_dict() if self.timing is not None else None),
        }

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> HttpResponse:
        """
        Deserialize a response.
        """

        response = cls(
            request_id=data["request_id"],
            status=data["status"],
            status_text=data.get(
                "status_text",
                "",
            ),
            url=data.get(
                "url",
                "",
            ),
            mime_type=data.get(
                "mime_type",
            ),
            encoding=data.get(
                "encoding",
            ),
            content_length=data.get(
                "content_length",
            ),
            body=data.get(
                "body",
            ),
            redirected=data.get(
                "redirected",
                False,
            ),
            server_ip=data.get(
                "server_ip",
            ),
            timing=(RequestTiming.from_dict(data["timing"]) if data.get("timing") else None),
        )

        response.headers.extend(
            [
                HttpHeader.from_dict(item)
                for item in data.get(
                    "headers",
                    [],
                )
            ]
        )

        return response

    def __str__(self) -> str:
        return f"{self.status} {self.url}"
