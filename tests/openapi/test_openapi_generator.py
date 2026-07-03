from __future__ import annotations

from jit.discovery.api_mapper import ApiMapper
from jit.entities.http_request import HttpRequest
from jit.entities.http_response import HttpResponse
from jit.openapi.openapi_generator import OpenApiGenerator


def make_request() -> HttpRequest:
    return HttpRequest(
        id="1",
        method="POST",
        url="https://api.example.com/products",
        body={
            "name": "Laptop",
            "price": 100,
        },
    )


def make_response() -> HttpResponse:
    return HttpResponse(
        request_id="1",
        status=200,
        body={
            "id": 1,
            "name": "Laptop",
            "price": 100,
        },
    )


def test_generate_document():

    mapper = ApiMapper()

    mapper.add(
        make_request(),
        make_response(),
    )

    document = OpenApiGenerator.generate(mapper)

    assert document.title == "Discovered API"

    assert document.version == "1.0.0"

    assert len(document.paths) == 1


def test_generate_request_schema():

    mapper = ApiMapper()

    mapper.add(
        make_request(),
    )

    document = OpenApiGenerator.generate(mapper)

    path = document.get_path("/products")

    assert path is not None

    operation = path.get_operation("POST")

    assert operation is not None

    assert operation.request_body is not None

    assert "name" in operation.request_body.properties

    assert "price" in operation.request_body.properties


def test_generate_response_schema():

    mapper = ApiMapper()

    mapper.add(
        make_request(),
        make_response(),
    )

    document = OpenApiGenerator.generate(mapper)

    path = document.get_path("/products")

    assert path is not None

    operation = path.get_operation("POST")

    assert operation is not None

    assert 200 in operation.responses

    schema = operation.responses[200]

    assert "id" in schema.properties

    assert "name" in schema.properties

    assert "price" in schema.properties
