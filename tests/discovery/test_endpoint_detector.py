from __future__ import annotations

from jit.discovery.endpoint_detector import EndpointDetector
from jit.entities.http_request import HttpRequest
from jit.entities.http_response import HttpResponse


def make_request(
    *,
    method: str = "GET",
    url: str = "https://api.example.com/products",
) -> HttpRequest:
    return HttpRequest(
        method=method,
        url=url,
    )


def make_response(
    request: HttpRequest,
    *,
    status: int = 200,
) -> HttpResponse:
    return HttpResponse(
        request_id=request.id,
        url=request.url,
        status=status,
    )


def test_detector_starts_empty():
    detector = EndpointDetector()

    assert len(detector) == 0
    assert detector.all() == []


def test_add_request_creates_endpoint():
    detector = EndpointDetector()

    request = make_request()

    endpoint = detector.add_request(request)

    assert endpoint.path == "/products"
    assert endpoint.method == "GET"

    assert len(detector) == 1


def test_same_endpoint_is_reused():
    detector = EndpointDetector()

    first = make_request()
    second = make_request()

    endpoint1 = detector.add_request(first)
    endpoint2 = detector.add_request(second)

    assert endpoint1 is endpoint2
    assert endpoint1.request_count == 2


def test_different_methods_create_new_endpoint():
    detector = EndpointDetector()

    detector.add_request(
        make_request(method="GET")
    )

    detector.add_request(
        make_request(method="POST")
    )

    assert len(detector) == 2


def test_different_paths_create_new_endpoint():
    detector = EndpointDetector()

    detector.add_request(
        make_request(
            url="https://api.example.com/products"
        )
    )

    detector.add_request(
        make_request(
            url="https://api.example.com/orders"
        )
    )

    assert len(detector) == 2


def test_get_existing_endpoint():
    detector = EndpointDetector()

    detector.add_request(
        make_request()
    )

    endpoint = detector.get(
        "GET",
        "/products",
    )

    assert endpoint is not None
    assert endpoint.path == "/products"


def test_get_missing_endpoint():
    detector = EndpointDetector()

    assert detector.get(
        "GET",
        "/missing",
    ) is None


def test_add_response():
    detector = EndpointDetector()

    request = make_request()

    endpoint = detector.add_request(request)

    response = make_response(request)

    detector.add_response(response)

    assert endpoint.response_count == 1
    assert endpoint.latest_response is response


def test_response_without_request_is_ignored():
    detector = EndpointDetector()

    request = make_request()

    response = make_response(request)

    detector.add_response(response)

    assert len(detector) == 0


def test_all_returns_every_endpoint():
    detector = EndpointDetector()

    detector.add_request(
        make_request(
            url="https://api.example.com/products"
        )
    )

    detector.add_request(
        make_request(
            url="https://api.example.com/orders"
        )
    )

    endpoints = detector.all()

    assert len(endpoints) == 2


def test_clear():
    detector = EndpointDetector()

    detector.add_request(make_request())

    detector.clear()

    assert len(detector) == 0
    assert detector.all() == []


def test_len():
    detector = EndpointDetector()

    detector.add_request(make_request())

    assert len(detector) == 1


def test_iter():
    detector = EndpointDetector()

    detector.add_request(make_request())

    endpoints = list(detector)

    assert len(endpoints) == 1


def test_method_is_normalized():
    detector = EndpointDetector()

    detector.add_request(
        make_request(method="get")
    )

    endpoint = detector.get(
        "GET",
        "/products",
    )

    assert endpoint is not None


def test_multiple_responses():
    detector = EndpointDetector()

    request = make_request()

    endpoint = detector.add_request(request)

    detector.add_response(
        make_response(request, status=200)
    )

    detector.add_response(
        make_response(request, status=304)
    )

    assert endpoint.response_count == 2


def test_latest_response():
    detector = EndpointDetector()

    request = make_request()

    endpoint = detector.add_request(request)

    first = make_response(
        request,
        status=200,
    )

    second = make_response(
        request,
        status=500,
    )

    detector.add_response(first)
    detector.add_response(second)

    assert endpoint.latest_response is second
