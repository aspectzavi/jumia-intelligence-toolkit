from __future__ import annotations

from jit.entities.header_collection import HeaderCollection
from jit.entities.http_header import HttpHeader
from jit.serializers.header_collection_serializer import (
    HeaderCollectionSerializer,
)


def test_to_dict() -> None:
    headers = HeaderCollection()

    headers.add(
        HttpHeader(
            name="Content-Type",
            value="application/json",
        )
    )

    headers.add(
        HttpHeader(
            name="Accept",
            value="*/*",
        )
    )

    result = HeaderCollectionSerializer.to_dict(headers)

    assert result == [
        {
            "name": "content-type",
            "value": "application/json",
        },
        {
            "name": "accept",
            "value": "*/*",
        },
    ]


def test_from_dict() -> None:
    data = [
        {
            "name": "Host",
            "value": "jumia.co.ke",
        },
        {
            "name": "Accept",
            "value": "application/json",
        },
    ]

    headers = HeaderCollectionSerializer.from_dict(data)

    assert len(headers) == 2
    assert headers["host"] == "jumia.co.ke"
    assert headers["accept"] == "application/json"


def test_round_trip() -> None:
    original = HeaderCollection()

    original.add(
        HttpHeader(
            name="Authorization",
            value="Bearer token",
        )
    )

    original.add(
        HttpHeader(
            name="User-Agent",
            value="Playwright",
        )
    )

    restored = HeaderCollectionSerializer.from_dict(
        HeaderCollectionSerializer.to_dict(original)
    )

    assert restored == original
