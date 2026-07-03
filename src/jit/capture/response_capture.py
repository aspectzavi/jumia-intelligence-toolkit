from __future__ import annotations

from collections.abc import Iterator

from jit.entities.http_response import HttpResponse


class ResponseCapture:
    """
    Stores captured HTTP responses.
    """

    def __init__(self) -> None:
        self._responses: list[HttpResponse] = []

    def add(
        self,
        response: HttpResponse,
    ) -> None:
        """
        Store a response.
        """

        self._responses.append(response)

    @property
    def latest(self) -> HttpResponse | None:
        """
        Return the most recently captured response.
        """

        if not self._responses:
            return None

        return self._responses[-1]

    def clear(self) -> None:
        """
        Remove all captured responses.
        """

        self._responses.clear()

    def __len__(self) -> int:
        return len(self._responses)

    def __iter__(self) -> Iterator[HttpResponse]:
        return iter(self._responses)
