from __future__ import annotations

from jit.discovery.api_mapper import ApiMapper
from jit.entities.http_request import HttpRequest
from jit.entities.http_response import HttpResponse


def make_request(
    url: str,
    method: str = "GET",
) -> HttpRequest:
    return HttpRequest(
        id="1",
        method=method,
        url=url,
    )


def test_create_empty_mapper():
    mapper = ApiMapper()

    assert len(mapper) == 0


def test_add_request():
    mapper = ApiMapper()

    mapper.add(
        make_request(
            "https://api.example.com/products",
        )
    )

    assert len(mapper) == 1


def test_get_endpoint():
    mapper = ApiMapper()

    mapper.add(
        make_request(
            "https://api.example.com/products",
        )
    )

    endpoint = mapper.get(
        "GET",
        "/products",
    )

    assert endpoint is not None
    assert endpoint.path == "/products"


def test_clear():
    mapper = ApiMapper()

    mapper.add(
        make_request(
            "https://api.example.com/products",
        )
    )

    mapper.clear()

    assert len(mapper) == 0


def test_iter():
    mapper = ApiMapper()

    mapper.add(
        make_request(
            "https://api.example.com/products",
        )
    )

    mapper.add(
        make_request(
            "https://api.example.com/orders",
        )
    )

    paths = {
        endpoint.path
        for endpoint in mapper
    }

    assert paths == {
        "/products",
        "/orders",
    }

def make_response(
    request_id: str = "1",
    status: int = 200,
) -> HttpResponse:
    return HttpResponse(
        request_id=request_id,
        status=status,
    )


def test_add_request_and_response():
    mapper = ApiMapper()

    request = make_request(
        "https://api.example.com/products",
    )

    response = make_response()

    endpoint = mapper.add(
        request,
        response,
    )

    assert endpoint.response_count == 1
    assert endpoint.latest_response is response


def test_response_without_matching_request():
    mapper = ApiMapper()

    response = make_response(
        request_id="unknown",
    )

    # Should not raise
    mapper._detector.add_response(response)

    assert len(mapper) == 0
