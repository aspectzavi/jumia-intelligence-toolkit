from __future__ import annotations

from typing import Protocol

from jit.entities.http_header import HttpHeader
from jit.entities.http_request import HttpRequest


class RequestLike(Protocol):
    """
    Protocol representing the subset of a Playwright Request
    used by RequestMapper.
    """

    @property
    def url(self) -> str:
        ...

    @property
    def method(self) -> str:
        ...

    @property
    def resource_type(self) -> str:
        ...

    @property
    def headers(self) -> dict[str, str]:
        ...

    @property
    def post_data(self) -> str | None:
        ...


class RequestMapper:
    """
    Converts Playwright Request-like objects into HttpRequest entities.
    """

    @classmethod
    def map(
        cls,
        request: RequestLike,
    ) -> HttpRequest:
        """
        Convert a Playwright request into an HttpRequest entity.
        """

        http_request = HttpRequest(
            method=request.method,
            url=request.url,
            resource_type=request.resource_type,
            body=request.post_data,
        )

        for name, value in request.headers.items():
            http_request.add_header(
                HttpHeader(
                    name=name,
                    value=value,
                )
            )

        return http_request
