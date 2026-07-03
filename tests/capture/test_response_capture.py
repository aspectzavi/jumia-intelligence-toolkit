from __future__ import annotations

from jit.capture.response_capture import ResponseCapture
from jit.entities.http_response import HttpResponse


def test_add_response():
    capture = ResponseCapture()

    response = HttpResponse(
        request_id="1",
        status=200,
    )

    capture.add(response)

    assert len(capture) == 1


def test_latest_response():
    capture = ResponseCapture()

    response = HttpResponse(
        request_id="1",
        status=200,
    )

    capture.add(response)

    assert capture.latest is response
