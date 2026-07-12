from __future__ import annotations

from jit.entities.http_header import HttpHeader
from jit.entities.http_response import HttpResponse
from jit.entities.request_timing import RequestTiming
from jit.serializers.http_response_serializer import (
    HttpResponseSerializer,
)


def make_response() -> HttpResponse:
    response = HttpResponse(
        request_id="request-123",
        status=200,
        status_text="OK",
        url="https://www.jumia.co.ke/api/products",
        mime_type="application/json",
        encoding="utf-8",
        content_length=128,
        body={
            "success": True,
        },
        redirected=False,
        server_ip="127.0.0.1",
        timing=RequestTiming.start_now(),
    )

    response.add_header(
        HttpHeader(
            name="Content-Type",
            value="application/json",
        )
    )

    response.add_header(
        HttpHeader(
            name="Cache-Control",
            value="no-cache",
        )
    )

    assert response.timing is not None
    response.timing.finish()

    return response


def test_to_dict() -> None:
    response = make_response()

    data = HttpResponseSerializer.to_dict(
        response,
    )

    assert data["request_id"] == "request-123"
    assert data["status"] == 200
    assert data["status_text"] == "OK"
    assert data["mime_type"] == "application/json"

    assert len(data["headers"]) == 2
    assert data["headers"][0]["name"] == "content-type"

    assert data["timing"]["started_at"] is not None


def test_from_dict() -> None:
    original = make_response()

    restored = HttpResponseSerializer.from_dict(
        HttpResponseSerializer.to_dict(
            original,
        )
    )

    assert restored.request_id == original.request_id
    assert restored.status == original.status
    assert restored.status_text == original.status_text
    assert restored.url == original.url
    assert restored.mime_type == original.mime_type
    assert restored.encoding == original.encoding
    assert restored.content_length == original.content_length
    assert restored.body == original.body
    assert restored.redirected == original.redirected
    assert restored.server_ip == original.server_ip

    assert (
        restored.headers["content-type"]
        == "application/json"
    )

    assert restored.timing is not None
    assert original.timing is not None

    assert (
        restored.timing.started_at
        == original.timing.started_at
    )

    assert (
        restored.timing.ended_at
        == original.timing.ended_at
    )


def test_round_trip() -> None:
    original = make_response()

    restored = HttpResponseSerializer.from_dict(
        HttpResponseSerializer.to_dict(
            original,
        )
    )

    assert (
        HttpResponseSerializer.to_dict(
            restored,
        )
        == HttpResponseSerializer.to_dict(
            original,
        )
    )
