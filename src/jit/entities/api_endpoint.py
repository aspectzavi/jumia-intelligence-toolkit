from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from jit.core.enums import RequestType
from jit.entities.http_request import HttpRequest
from jit.entities.http_response import HttpResponse
from jit.entities.schema import Schema


@dataclass(slots=True)
class ApiEndpoint:
    """
    Represents a discovered API endpoint.

    Multiple captured requests can belong to the same endpoint.
    """

    path: str

    method: str

    request_type: RequestType = RequestType.API

    requests: list[HttpRequest] = field(default_factory=list)

    responses: list[HttpResponse] = field(default_factory=list)

    request_schema: Schema | None = None

    response_schema: Schema | None = None

    tags: set[str] = field(default_factory=set)

    description: str | None = None

    #
    # -------- Intelligence --------
    #

    status_codes: dict[int, int] = field(default_factory=dict)

    content_types: dict[str, int] = field(default_factory=dict)

    examples: list[Any] = field(default_factory=list)

    confidence: float = 0.0

    @property
    def request_count(self) -> int:
        return len(self.requests)

    @property
    def response_count(self) -> int:
        return len(self.responses)

    @property
    def latest_request(self) -> HttpRequest | None:
        if not self.requests:
            return None

        return self.requests[-1]

    @property
    def latest_response(self) -> HttpResponse | None:
        if not self.responses:
            return None

        return self.responses[-1]

    def add_request(
        self,
        request: HttpRequest,
    ) -> None:
        self.requests.append(request)

    def add_response(
        self,
        response: HttpResponse,
    ) -> None:
        self.responses.append(response)

    def add_tag(
        self,
        tag: str,
    ) -> None:
        self.tags.add(tag)

    #
    # ---------- Intelligence helpers ----------
    #

    def add_status_code(
        self,
        status_code: int,
    ) -> None:
        self.status_codes[status_code] = self.status_codes.get(status_code, 0) + 1

    def add_content_type(
        self,
        content_type: str | None,
    ) -> None:
        if not content_type:
            return

        content_type = content_type.split(";", 1)[0].strip().lower()

        self.content_types[content_type] = (
            self.content_types.get(content_type, 0) + 1
        )

    def add_example(
        self,
        payload: Any,
    ) -> None:
        """
        Store one example response.

        Limit the number of stored examples so long-running
        captures do not consume excessive memory.
        """

        if payload is None:
            return

        if len(self.examples) >= 10:
            return

        self.examples.append(payload)

    @property
    def primary_status_code(self) -> int | None:
        if not self.status_codes:
            return None

        return max(
            self.status_codes.items(),
            key=lambda item: item[1],
        )[0]

    @property
    def primary_content_type(self) -> str | None:
        if not self.content_types:
            return None

        return max(
            self.content_types.items(),
            key=lambda item: item[1],
        )[0]

    def __str__(self) -> str:
        return f"{self.method} {self.path}"
