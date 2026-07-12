from __future__ import annotations

from jit.entities.http_cookie import HttpCookie
from jit.entities.http_header import HttpHeader
from jit.entities.http_request import HttpRequest
from jit.serializers.http_request_serializer import (
    HttpRequestSerializer,
)


def make_request() -> HttpRequest:
    request = HttpRequest(
        url="https://www.jumia.co.ke/api/products",
        method="POST",
        resource_type="xhr",
        frame_url="https://www.jumia.co.ke",
        is_navigation=False,
        post_data='{"id":1}',
        body={
            "id": 1,
        },
    )

    request.add_header(
        HttpHeader(
            name="Content-Type",
            value="application/json",
        )
    )

    request.add_header(
        HttpHeader(
            name="Authorization",
            value="Bearer token",
        )
    )

    request.add_cookie(
        HttpCookie(
            name="session",
            value="abc123",
            domain=".jumia.co.ke",
            secure=True,
        )
    )

    request.timing.finish()

    return request


def test_to_dict() -> None:
    request = make_request()

    data = HttpRequestSerializer.to_dict(
        request
    )

    assert data["url"] == request.url
    assert data["method"] == "POST"
    assert data["resource_type"] == "xhr"

    assert len(data["headers"]) == 2
    assert len(data["cookies"]) == 1

    assert data["headers"][0]["name"] == "content-type"
    assert data["cookies"][0]["name"] == "session"

    assert data["timing"]["started_at"] is not None


def test_from_dict() -> None:
    original = make_request()

    data = HttpRequestSerializer.to_dict(
        original
    )

    restored = HttpRequestSerializer.from_dict(
        data
    )

    assert restored.id == original.id
    assert restored.url == original.url
    assert restored.method == original.method
    assert restored.resource_type == original.resource_type

    assert restored.headers["content-type"] == (
        "application/json"
    )

    assert restored.cookies[0].name == "session"
    assert restored.cookies[0].value == "abc123"

    assert restored.body == {"id": 1}

    assert restored.timing.started_at == (
        original.timing.started_at
    )

    assert restored.timing.ended_at == (
        original.timing.ended_at
    )


def test_round_trip() -> None:
    original = make_request()

    restored = HttpRequestSerializer.from_dict(
        HttpRequestSerializer.to_dict(
            original
        )
    )

    assert (
        HttpRequestSerializer.to_dict(restored)
        == HttpRequestSerializer.to_dict(original)
    )
