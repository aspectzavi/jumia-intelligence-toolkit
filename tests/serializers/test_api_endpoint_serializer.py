from __future__ import annotations

from jit.core.enums import RequestType
from jit.entities.api_endpoint import ApiEndpoint
from jit.entities.http_request import HttpRequest
from jit.entities.http_response import HttpResponse
from jit.entities.schema import Schema
from jit.entities.schema_field import SchemaField
from jit.serializers.api_endpoint_serializer import (
    ApiEndpointSerializer,
)


def make_request() -> HttpRequest:
    return HttpRequest(
        url="https://www.jumia.co.ke/api/products",
        method="POST",
    )


def make_response() -> HttpResponse:
    return HttpResponse(
        request_id="request-123",
        status=200,
        status_text="OK",
        url="https://www.jumia.co.ke/api/products",
    )


def make_schema() -> Schema:
    schema = Schema()

    schema.add_field(
        SchemaField(
            name="price",
            field_type="integer",
        )
    )

    return schema


def make_endpoint() -> ApiEndpoint:
    endpoint = ApiEndpoint(
        path="/api/products",
        method="POST",
        request_type=RequestType.API,
        description="Product endpoint",
    )

    endpoint.add_tag("catalog")
    endpoint.add_tag("products")

    endpoint.add_request(make_request())
    endpoint.add_response(make_response())

    endpoint.request_schema = make_schema()
    endpoint.response_schema = make_schema()

    return endpoint


def test_to_dict() -> None:
    endpoint = make_endpoint()

    data = ApiEndpointSerializer.to_dict(endpoint)

    assert data["path"] == "/api/products"
    assert data["method"] == "POST"
    assert data["request_type"] == RequestType.API.value
    assert data["description"] == "Product endpoint"

    assert sorted(data["tags"]) == [
        "catalog",
        "products",
    ]

    assert len(data["requests"]) == 1
    assert len(data["responses"]) == 1

    assert data["request_schema"] is not None
    assert data["response_schema"] is not None


def test_from_dict() -> None:
    original = make_endpoint()

    restored = ApiEndpointSerializer.from_dict(
        ApiEndpointSerializer.to_dict(original)
    )

    assert restored.path == original.path
    assert restored.method == original.method
    assert restored.request_type == original.request_type
    assert restored.description == original.description

    assert restored.tags == original.tags

    assert len(restored.requests) == 1
    assert len(restored.responses) == 1

    assert restored.request_schema is not None
    assert restored.response_schema is not None

    assert (
        restored.request_schema.fields[0].name
        == "price"
    )

    assert (
        restored.response_schema.fields[0].field_type
        == "integer"
    )


def test_round_trip() -> None:
    original = make_endpoint()

    restored = ApiEndpointSerializer.from_dict(
        ApiEndpointSerializer.to_dict(original)
    )

    assert (
        ApiEndpointSerializer.to_dict(restored)
        == ApiEndpointSerializer.to_dict(original)
    )
