from __future__ import annotations

from collections.abc import Iterator

from jit.entities.http_request import HttpRequest


class RequestCapture:
    """
    Stores captured HTTP requests.
    """

    def __init__(self) -> None:
        self._requests: list[HttpRequest] = []

    def add(
        self,
        request: HttpRequest,
    ) -> None:
        """
        Store a request.
        """

        self._requests.append(request)

    @property
    def latest(self) -> HttpRequest | None:
        """
        Return the most recently captured request.
        """

        if not self._requests:
            return None

        return self._requests[-1]

    def clear(self) -> None:
        """
        Remove all captured requests.
        """

        self._requests.clear()

    def __len__(self) -> int:
        return len(self._requests)

    def __iter__(self) -> Iterator[HttpRequest]:
        return iter(self._requests)
