from __future__ import annotations

from jit.capture.request_capture import RequestCapture
from jit.entities.http_request import HttpRequest


def test_add_request():
    capture = RequestCapture()

    request = HttpRequest(
        method="GET",
        url="https://example.com",
    )

    capture.add(request)

    assert len(capture) == 1


def test_latest_request():
    capture = RequestCapture()

    request = HttpRequest(
        method="GET",
        url="https://example.com",
    )

    capture.add(request)

    assert capture.latest is request
