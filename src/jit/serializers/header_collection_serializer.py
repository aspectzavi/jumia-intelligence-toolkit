from __future__ import annotations

from typing import Any

from jit.entities.header_collection import HeaderCollection
from jit.serializers.http_header_serializer import (
    HttpHeaderSerializer,
)


class HeaderCollectionSerializer:
    """
    Serializes HeaderCollection objects.
    """

    @staticmethod
    def to_dict(
        headers: HeaderCollection,
    ) -> list[dict[str, Any]]:
        """
        Serialize a HeaderCollection.
        """

        return [
            HttpHeaderSerializer.to_dict(header)
            for header in headers
        ]

    @staticmethod
    def from_dict(
        data: list[dict[str, Any]],
    ) -> HeaderCollection:
        """
        Deserialize a HeaderCollection.
        """

        return HeaderCollection(
            [
                HttpHeaderSerializer.from_dict(item)
                for item in data
            ]
        )
