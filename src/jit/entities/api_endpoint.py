from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from jit.core.enums import RequestType
from jit.entities.http_request import HttpRequest
from jit.entities.http_response import HttpResponse


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

    tags: set[str] = field(default_factory=set)

    description: str | None = None

    @property
    def request_count(self) -> int:
        """
        Number of captured requests.
        """
        return len(self.requests)

    @property
    def response_count(self) -> int:
        """
        Number of captured responses.
        """
        return len(self.responses)

    @property
    def latest_request(self) -> HttpRequest | None:
        """
        Most recently added request.
        """
        if not self.requests:
            return None

        return self.requests[-1]

    @property
    def latest_response(self) -> HttpResponse | None:
        """
        Most recently added response.
        """
        if not self.responses:
            return None

        return self.responses[-1]

    def add_request(
        self,
        request: HttpRequest,
    ) -> None:
        """
        Attach a request to this endpoint.
        """
        self.requests.append(request)

    def add_response(
        self,
        response: HttpResponse,
    ) -> None:
        """
        Attach a response to this endpoint.
        """
        self.responses.append(response)

    def add_tag(
        self,
        tag: str,
    ) -> None:
        """
        Add a descriptive tag.
        """
        self.tags.add(tag)

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize endpoint.
        """

        return {
            "path": self.path,
            "method": self.method,
            "request_type": self.request_type.value,
            "description": self.description,
            "tags": sorted(self.tags),
            "requests": [
                request.to_dict()
                for request in self.requests
            ],
            "responses": [
                response.to_dict()
                for response in self.responses
            ],
        }

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> ApiEndpoint:
        """
        Deserialize endpoint.
        """

        endpoint = cls(
            path=data["path"],
            method=data["method"],
            request_type=RequestType(
                data.get(
                    "request_type",
                    RequestType.API.value,
                )
            ),
            description=data.get("description"),
        )

        endpoint.tags.update(
            data.get(
                "tags",
                [],
            )
        )

        endpoint.requests.extend(
            HttpRequest.from_dict(item)
            for item in data.get(
                "requests",
                [],
            )
        )

        endpoint.responses.extend(
            HttpResponse.from_dict(item)
            for item in data.get(
                "responses",
                [],
            )
        )

        return endpoint

    def __str__(self) -> str:
        return f"{self.method} {self.path}"
