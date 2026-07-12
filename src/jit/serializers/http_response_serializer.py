from __future__ import annotations

from typing import Any

from jit.entities.http_response import HttpResponse


class HttpResponseSerializer:
    """
    Serializes HttpResponse objects.

    This serializer delegates serialization to the entity,
    keeping serialization logic centralized and avoiding
    circular imports.
    """

    @staticmethod
    def to_dict(
        response: HttpResponse,
    ) -> dict[str, Any]:
        """
        Serialize a HttpResponse.
        """

        return response.to_dict()

    @staticmethod
    def from_dict(
        data: dict[str, Any],
    ) -> HttpResponse:
        """
        Deserialize a HttpResponse.
        """

        return HttpResponse.from_dict(data)
