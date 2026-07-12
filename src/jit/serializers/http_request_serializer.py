from __future__ import annotations

from typing import Any

from jit.entities.http_request import HttpRequest


class HttpRequestSerializer:
    """
    Serializes HttpRequest objects.

    This serializer delegates serialization to the entity,
    keeping all serialization logic in one place and avoiding
    circular imports.
    """

    @staticmethod
    def to_dict(
        request: HttpRequest,
    ) -> dict[str, Any]:
        """
        Serialize a HttpRequest.
        """

        return request.to_dict()

    @staticmethod
    def from_dict(
        data: dict[str, Any],
    ) -> HttpRequest:
        """
        Deserialize a HttpRequest.
        """

        return HttpRequest.from_dict(data)
