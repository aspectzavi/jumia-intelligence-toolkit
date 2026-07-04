from __future__ import annotations

from jit.discovery.schema_manager import SchemaManager
from jit.entities.api_endpoint import ApiEndpoint


def test_request_schema_created() -> None:
    endpoint = ApiEndpoint(
        path="/products",
        method="GET",
    )

    SchemaManager.update_request_schema(
        endpoint,
        {
            "id": 1,
            "name": "Phone",
        },
    )

    assert endpoint.request_schema is not None

    id_field = endpoint.request_schema.get_field("id")
    name_field = endpoint.request_schema.get_field("name")

    assert id_field is not None
    assert name_field is not None

    assert id_field.field_type == "integer"
    assert name_field.field_type == "string"


def test_request_schema_merges() -> None:
    endpoint = ApiEndpoint(
        path="/products",
        method="GET",
    )

    SchemaManager.update_request_schema(
        endpoint,
        {
            "id": 1,
        },
    )

    SchemaManager.update_request_schema(
        endpoint,
        {
            "price": 99.5,
        },
    )

    assert endpoint.request_schema is not None

    assert endpoint.request_schema.get_field("id") is not None
    assert endpoint.request_schema.get_field("price") is not None


def test_response_schema_created() -> None:
    endpoint = ApiEndpoint(
        path="/products",
        method="GET",
    )

    SchemaManager.update_response_schema(
        endpoint,
        {
            "success": True,
            "count": 10,
        },
    )

    assert endpoint.response_schema is not None

    success_field = endpoint.response_schema.get_field("success")
    count_field = endpoint.response_schema.get_field("count")

    assert success_field is not None
    assert count_field is not None

    assert success_field.field_type == "boolean"
    assert count_field.field_type == "integer"


def test_response_schema_merges() -> None:
    endpoint = ApiEndpoint(
        path="/products",
        method="GET",
    )

    SchemaManager.update_response_schema(
        endpoint,
        {
            "id": 1,
        },
    )

    SchemaManager.update_response_schema(
        endpoint,
        {
            "name": "Laptop",
        },
    )

    assert endpoint.response_schema is not None

    assert endpoint.response_schema.get_field("id") is not None
    assert endpoint.response_schema.get_field("name") is not None


def test_request_schema_ignores_non_dict() -> None:
    endpoint = ApiEndpoint(
        path="/products",
        method="GET",
    )

    SchemaManager.update_request_schema(
        endpoint,
        ["not", "a", "dict"],
    )

    assert endpoint.request_schema is None


def test_response_schema_ignores_non_dict() -> None:
    endpoint = ApiEndpoint(
        path="/products",
        method="GET",
    )

    SchemaManager.update_response_schema(
        endpoint,
        "not a dict",
    )

    assert endpoint.response_schema is None
