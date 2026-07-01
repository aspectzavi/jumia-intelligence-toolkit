from __future__ import annotations

from jit.discovery.api_mapper import ApiMapper
from jit.entities.http_request import HttpRequest


def make_request(body: object) -> HttpRequest:
    return HttpRequest(
        id="1",
        method="POST",
        url="https://api.example.com/products",
        body=body,
    )


def test_detect_request_schema():
    mapper = ApiMapper()

    mapper.add(
        make_request(
            {
                "id": 1,
                "name": "Laptop",
            }
        )
    )

    endpoint = mapper.get(
        "POST",
        "/products",
    )

    assert endpoint is not None
    assert endpoint.request_schema is not None

    id_field = endpoint.request_schema.get_field("id")
    name_field = endpoint.request_schema.get_field("name")

    assert id_field is not None
    assert name_field is not None

    assert id_field.field_type == "integer"
    assert name_field.field_type == "string"


def test_schema_merges_between_requests():
    mapper = ApiMapper()

    mapper.add(
        make_request(
            {
                "id": 1,
            }
        )
    )

    mapper.add(
        make_request(
            {
                "id": 2,
                "price": 100,
            }
        )
    )

    endpoint = mapper.get(
        "POST",
        "/products",
    )

    assert endpoint is not None
    assert endpoint.request_schema is not None

    price_field = endpoint.request_schema.get_field("price")

    assert price_field is not None
    assert price_field.field_type == "integer"
