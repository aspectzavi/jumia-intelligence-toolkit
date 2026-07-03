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
    the API discovery pipeline.
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
        """
        Handle a Playwright request event.
        """

        http_request = RequestMapper.map(request)

        self.last_request = http_request

        self.mapper.add(http_request)

    def on_response(
        self,
        response: ResponseLike,
    ) -> None:
        """
        Handle a Playwright response event.
        """

        if self.last_request is None:
            return

        http_response = ResponseMapper.map(
            request_id=self.last_request.id,
            response=response,
        )

        self.mapper.add_response(http_response)
