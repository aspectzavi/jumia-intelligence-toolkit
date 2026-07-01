from __future__ import annotations

from jit.discovery.api_mapper import ApiMapper
from jit.entities.http_request import HttpRequest
from jit.entities.http_response import HttpResponse


def make_request() -> HttpRequest:
    return HttpRequest(
        id="1",
        method="GET",
        url="https://api.example.com/products",
    )


def make_response(
    body: object,
) -> HttpResponse:
    return HttpResponse(
        request_id="1",
        status=200,
        body=body,
    )


def test_detect_response_schema():
    mapper = ApiMapper()

    mapper.add(
        make_request(),
        make_response(
            {
                "id": 1,
                "name": "Laptop",
            }
        ),
    )

    endpoint = mapper.get(
        "GET",
        "/products",
    )

    assert endpoint is not None
    assert endpoint.response_schema is not None

    id_field = endpoint.response_schema.get_field("id")
    name_field = endpoint.response_schema.get_field("name")

    assert id_field is not None
    assert id_field.field_type == "integer"

    assert name_field is not None
    assert name_field.field_type == "string"


def test_merge_response_schema():
    mapper = ApiMapper()

    mapper.add(
        make_request(),
        make_response(
            {
                "id": 1,
            }
        ),
    )

    mapper.add(
        make_request(),
        make_response(
            {
                "id": 2,
                "price": 100,
            }
        ),
    )

    endpoint = mapper.get(
        "GET",
        "/products",
    )

    assert endpoint is not None
    assert endpoint.response_schema is not None

    price_field = endpoint.response_schema.get_field("price")

    assert price_field is not None
    assert price_field.field_type == "integer"
