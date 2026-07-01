from __future__ import annotations

from jit.entities.http_request import HttpRequest
from jit.entities.http_response import HttpResponse


class NetworkRecorder:
    """
    Stores captured HTTP requests and responses.

    This class is transport-agnostic and does not depend on
    Playwright or any browser implementation.
    """

    def __init__(self) -> None:
        self._requests: list[HttpRequest] = []
        self._responses: list[HttpResponse] = []

    @property
    def requests(self) -> list[HttpRequest]:
        """
        Return all recorded requests.
        """
        return self._requests

    @property
    def responses(self) -> list[HttpResponse]:
        """
        Return all recorded responses.
        """
        return self._responses

    def record_request(
        self,
        request: HttpRequest,
    ) -> None:
        """
        Record a request.
        """
        self._requests.append(request)

    def record_response(
        self,
        response: HttpResponse,
    ) -> None:
        """
        Record a response.
        """
        self._responses.append(response)

    def clear(self) -> None:
        """
        Remove all recorded traffic.
        """
        self._requests.clear()
        self._responses.clear()

    @property
    def request_count(self) -> int:
        return len(self._requests)

    @property
    def response_count(self) -> int:
        return len(self._responses)

    @property
    def total_count(self) -> int:
        return self.request_count + self.response_count
