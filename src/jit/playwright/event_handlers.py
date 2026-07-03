from __future__ import annotations

from jit.discovery.api_mapper import ApiMapper
from jit.entities.http_request import HttpRequest
from jit.playwright.request_mapper import (
    RequestLike,
    RequestMapper,
)
from jit.playwright.response_mapper import (
    ResponseLike,
    ResponseMapper,
)


class EventHandlers:
    """
    Receives browser network events and forwards them into
    the discovery pipeline.
    """

    def __init__(
        self,
        mapper: ApiMapper,
    ) -> None:

        self.mapper = mapper

        self.last_request: HttpRequest | None = None

    def on_request(
        self,
        request: RequestLike,
    ) -> None:

        http_request = RequestMapper.map(request)

        self.last_request = http_request

        self.mapper.add(http_request)

    def on_response(
        self,
        *,
        request_id: str,
        response: ResponseLike,
    ) -> None:

        http_response = ResponseMapper.map(
            request_id=request_id,
            response=response,
        )

        self.mapper.add_response(http_response)
