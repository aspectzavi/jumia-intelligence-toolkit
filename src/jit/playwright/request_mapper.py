from __future__ import annotations

from typing import Protocol

from jit.entities.http_header import HttpHeader
from jit.entities.http_request import HttpRequest


class RequestLike(Protocol):
    """
    Protocol representing the subset of a Playwright Request
    that RequestMapper depends on.

    Any object exposing these attributes is compatible,
    including the real Playwright Request and test doubles.
    """

    url: str
    method: str
    resource_type: str
    headers: dict[str, str]
    post_data: str | None


class RequestMapper:
    """
    Converts Playwright Request-like objects into HttpRequest entities.
    """

    @classmethod
    def map(
        cls,
        request: RequestLike,
    ) -> HttpRequest:
        http_request = HttpRequest(
            url=request.url,
            method=request.method,
            resource_type=request.resource_type,
            post_data=request.post_data,
        )

        for name, value in request.headers.items():
            http_request.add_header(
                HttpHeader(
                    name=name,
                    value=value,
                )
            )

        return http_request
