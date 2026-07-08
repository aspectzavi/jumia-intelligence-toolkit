from __future__ import annotations

from jit.entities.http_header import HttpHeader


class HttpHeaderSerializer:
    """
    Serializes HttpHeader objects.
    """

    @staticmethod
    def to_dict(
        header: HttpHeader,
    ) -> dict[str, str]:
        """
        Serialize a header.
        """

        return {
            "name": header.name,
            "value": header.value,
        }

    @staticmethod
    def from_dict(
        data: dict[str, str],
    ) -> HttpHeader:
        """
        Deserialize a header.
        """

        return HttpHeader(
            name=data["name"],
            value=data["value"],
        )
