from __future__ import annotations

from typing import Protocol

from jit.entities.http_header import HttpHeader
from jit.entities.http_response import HttpResponse


class ResponseLike(Protocol):
    """
    Protocol representing the subset of a Playwright Response
    used by ResponseMapper.
    """

    @property
    def status(self) -> int:
        ...

    @property
    def status_text(self) -> str:
        ...

    @property
    def url(self) -> str:
        ...

    @property
    def headers(self) -> dict[str, str]:
        ...


class ResponseMapper:
    """
    Converts Playwright Response-like objects into HttpResponse entities.
    """

    @classmethod
    def map(
        cls,
        *,
        request_id: str,
        response: ResponseLike,
    ) -> HttpResponse:
        """
        Convert a Playwright response into an HttpResponse entity.
        """

        http_response = HttpResponse(
            request_id=request_id,
            status=response.status,
            status_text=response.status_text,
            url=response.url,
        )

        for name, value in response.headers.items():
            http_response.add_header(
                HttpHeader(
                    name=name,
                    value=value,
                )
            )

        return http_response
