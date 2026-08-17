from __future__ import annotations

from jit.entities.http_request import HttpRequest
from jit.entities.http_response import HttpResponse
from jit.entities.request_timing import RequestTiming
from jit.network.capture import CaptureSession


def make_request() -> HttpRequest:
    return HttpRequest(
        id="req-1",
        url="https://www.jumia.co.ke/api/products?page=1",
        method="GET",
        resource_type="xhr",
        timing=RequestTiming.start_now(),
    )


def make_response() -> HttpResponse:
    return HttpResponse(
        request_id="req-1",
        status=200,
        status_text="OK",
        url="https://www.jumia.co.ke/api/products?page=1",
        mime_type="application/json",
        timing=RequestTiming.start_now(),
    )


def test_new_capture_session() -> None:
    capture = CaptureSession()

    assert capture.request_count == 0
    assert capture.response_count == 0
    assert capture.endpoint_count == 0

    assert capture.requests == []
    assert capture.responses == []
    assert capture.endpoints == []


def test_process_discovers_endpoint() -> None:
    capture = CaptureSession()

    capture.recorder.record_request(
        make_request()
    )

    capture.process()

    assert capture.request_count == 1
    assert capture.endpoint_count == 1

    endpoint = capture.endpoints[0]

    assert endpoint.method == "GET"
    assert endpoint.path == "/api/products"
    assert endpoint.request_count == 1
    assert endpoint.response_count == 0


def test_process_attaches_response() -> None:
    capture = CaptureSession()

    capture.recorder.record_request(
        make_request()
    )

    capture.recorder.record_response(
        make_response()
    )

    capture.process()

    endpoint = capture.endpoints[0]

    assert endpoint.request_count == 1
    assert endpoint.response_count == 1

    assert endpoint.latest_response is not None
    assert endpoint.latest_response.status == 200


def test_clear() -> None:
    capture = CaptureSession()

    capture.recorder.record_request(
        make_request()
    )

    capture.recorder.record_response(
        make_response()
    )

    capture.process()

    assert capture.request_count == 1
    assert capture.response_count == 1
    assert capture.endpoint_count == 1

    capture.clear()

    assert capture.request_count == 0
    assert capture.response_count == 0
    assert capture.endpoint_count == 0

    assert capture.requests == []
    assert capture.responses == []
    assert capture.endpoints == []


def test_multiple_requests_same_endpoint() -> None:
    capture = CaptureSession()

    request1 = make_request()

    request2 = HttpRequest(
        id="req-2",
        url="https://www.jumia.co.ke/api/products?page=2",
        method="GET",
        resource_type="xhr",
        timing=RequestTiming.start_now(),
    )

    capture.recorder.record_request(request1)
    capture.recorder.record_request(request2)

    capture.process()

    assert capture.endpoint_count == 1

    endpoint = capture.endpoints[0]

    assert endpoint.request_count == 2


def test_multiple_endpoints() -> None:
    capture = CaptureSession()

    capture.recorder.record_request(
        HttpRequest(
            id="1",
            url="https://www.jumia.co.ke/api/products",
            method="GET",
            resource_type="xhr",
            timing=RequestTiming.start_now(),
        )
    )

    capture.recorder.record_request(
        HttpRequest(
            id="2",
            url="https://www.jumia.co.ke/api/cart",
            method="POST",
            resource_type="xhr",
            timing=RequestTiming.start_now(),
        )
    )

    capture.process()

    assert capture.endpoint_count == 2

    methods = {
        (endpoint.method, endpoint.path)
        for endpoint in capture.endpoints
    }

    assert ("GET", "/api/products") in methods
    assert ("POST", "/api/cart") in methods
