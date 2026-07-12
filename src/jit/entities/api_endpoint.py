from __future__ import annotations

from dataclasses import dataclass, field

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

    def __str__(self) -> str:
        return f"{self.method} {self.path}"
