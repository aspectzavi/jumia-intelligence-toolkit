from __future__ import annotations

from jit.core.enums import RequestType
from jit.entities.api_endpoint import ApiEndpoint
from jit.entities.http_request import HttpRequest
from jit.entities.http_response import HttpResponse


def make_request() -> HttpRequest:
    return HttpRequest(
        url="https://api.example.com/products",
        method="GET",
    )


def make_response() -> HttpResponse:
    return HttpResponse(
        request_id="req-1",
        url="https://api.example.com/products",
        status=200,
    )


def test_default_values():
    endpoint = ApiEndpoint(
        path="/products",
        method="GET",
    )

    assert endpoint.path == "/products"
    assert endpoint.method == "GET"
    assert endpoint.request_type == RequestType.API
    assert endpoint.requests == []
    assert endpoint.responses == []
    assert endpoint.tags == set()
    assert endpoint.description is None


def test_request_count():
    endpoint = ApiEndpoint(
        path="/products",
        method="GET",
    )

    endpoint.add_request(make_request())
    endpoint.add_request(make_request())

    assert endpoint.request_count == 2


def test_response_count():
    endpoint = ApiEndpoint(
        path="/products",
        method="GET",
    )

    endpoint.add_response(make_response())
    endpoint.add_response(make_response())

    assert endpoint.response_count == 2


def test_latest_request():
    endpoint = ApiEndpoint(
        path="/products",
        method="GET",
    )

    request1 = make_request()
    request2 = HttpRequest(
        url="https://api.example.com/orders",
        method="POST",
    )

    endpoint.add_request(request1)
    endpoint.add_request(request2)

    assert endpoint.latest_request is request2


def test_latest_response():
    endpoint = ApiEndpoint(
        path="/products",
        method="GET",
    )

    response1 = make_response()
    response2 = HttpResponse(
        request_id="req-2",
        url="https://api.example.com/orders",
        status=201,
    )

    endpoint.add_response(response1)
    endpoint.add_response(response2)

    assert endpoint.latest_response is response2


def test_latest_request_none():
    endpoint = ApiEndpoint(
        path="/products",
        method="GET",
    )

    assert endpoint.latest_request is None


def test_latest_response_none():
    endpoint = ApiEndpoint(
        path="/products",
        method="GET",
    )

    assert endpoint.latest_response is None


def test_add_tag():
    endpoint = ApiEndpoint(
        path="/products",
        method="GET",
    )

    endpoint.add_tag("catalog")
    endpoint.add_tag("public")
    endpoint.add_tag("catalog")

    assert endpoint.tags == {
        "catalog",
        "public",
    }


def test_to_dict():
    endpoint = ApiEndpoint(
        path="/products",
        method="GET",
        description="Product endpoint",
    )

    endpoint.add_tag("catalog")
    endpoint.add_request(make_request())
    endpoint.add_response(make_response())

    data = endpoint.to_dict()

    assert data["path"] == "/products"
    assert data["method"] == "GET"
    assert data["request_type"] == "api"
    assert data["description"] == "Product endpoint"
    assert data["tags"] == ["catalog"]
    assert len(data["requests"]) == 1
    assert len(data["responses"]) == 1


def test_from_dict():
    endpoint = ApiEndpoint(
        path="/products",
        method="GET",
        description="Product endpoint",
    )

    endpoint.add_tag("catalog")
    endpoint.add_request(make_request())
    endpoint.add_response(make_response())

    restored = ApiEndpoint.from_dict(
        endpoint.to_dict()
    )

    assert restored.path == endpoint.path
    assert restored.method == endpoint.method
    assert restored.request_type == RequestType.API
    assert restored.description == endpoint.description
    assert restored.tags == endpoint.tags
    assert restored.request_count == 1
    assert restored.response_count == 1


def test_string_representation():
    endpoint = ApiEndpoint(
        path="/products",
        method="GET",
    )

    assert str(endpoint) == "GET /products"
