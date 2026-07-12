from __future__ import annotations

from jit.entities.api_endpoint import ApiEndpoint
from jit.entities.schema import Schema
from jit.entities.schema_field import SchemaField


def test_assign_request_schema():
    endpoint = ApiEndpoint(
        path="/products",
        method="POST",
    )

    schema = Schema()

    schema.add_field(
        SchemaField(
            name="price",
            field_type="integer",
        )
    )

    endpoint.request_schema = schema

    assert endpoint.request_schema is schema
    assert (
        endpoint.request_schema.get_field("price")
        is not None
    )


def test_assign_response_schema():
    endpoint = ApiEndpoint(
        path="/products",
        method="POST",
    )

    schema = Schema()

    schema.add_field(
        SchemaField(
            name="id",
            field_type="integer",
        )
    )

    endpoint.response_schema = schema

    assert endpoint.response_schema is schema
    assert (
        endpoint.response_schema.get_field("id")
        is not None
    )

