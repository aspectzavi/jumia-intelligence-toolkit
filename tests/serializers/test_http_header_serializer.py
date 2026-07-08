from __future__ import annotations

from jit.entities.http_header import HttpHeader
from jit.serializers.http_header_serializer import (
    HttpHeaderSerializer,
)


def test_serializer_to_dict() -> None:
    header = HttpHeader(
        name="Content-Type",
        value="application/json",
    )

    data = HttpHeaderSerializer.to_dict(header)

    assert data == {
        "name": "content-type",
        "value": "application/json",
    }


def test_serializer_from_dict() -> None:
    data = {
        "name": "Host",
        "value": "jumia.co.ke",
    }

    header = HttpHeaderSerializer.from_dict(data)

    assert header.name == "host"
    assert header.value == "jumia.co.ke"


def test_round_trip() -> None:
    original = HttpHeader(
        name="Authorization",
        value="Bearer token",
    )

    restored = HttpHeaderSerializer.from_dict(
        HttpHeaderSerializer.to_dict(original),
    )

    assert restored == original
