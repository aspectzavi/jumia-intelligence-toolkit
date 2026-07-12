from __future__ import annotations

from typing import Any

from jit.core.enums import RequestType
from jit.entities.api_endpoint import ApiEndpoint
from jit.serializers.http_request_serializer import (
    HttpRequestSerializer,
)
from jit.serializers.http_response_serializer import (
    HttpResponseSerializer,
)
from jit.serializers.schema_serializer import (
    SchemaSerializer,
)


class ApiEndpointSerializer:
    """
    Serializes ApiEndpoint objects.
    """

    @staticmethod
    def to_dict(
        endpoint: ApiEndpoint,
    ) -> dict[str, Any]:
        """
        Serialize an ApiEndpoint.
        """

        return {
            "path": endpoint.path,
            "method": endpoint.method,
            "request_type": endpoint.request_type.value,
            "description": endpoint.description,
            "tags": sorted(endpoint.tags),
            "request_schema": (
                SchemaSerializer.to_dict(
                    endpoint.request_schema,
                )
                if endpoint.request_schema is not None
                else None
            ),
            "response_schema": (
                SchemaSerializer.to_dict(
                    endpoint.response_schema,
                )
                if endpoint.response_schema is not None
                else None
            ),
            "requests": [
                HttpRequestSerializer.to_dict(request)
                for request in endpoint.requests
            ],
            "responses": [
                HttpResponseSerializer.to_dict(response)
                for response in endpoint.responses
            ],
        }

    @staticmethod
    def from_dict(
        data: dict[str, Any],
    ) -> ApiEndpoint:
        """
        Deserialize an ApiEndpoint.
        """

        endpoint = ApiEndpoint(
            path=data["path"],
            method=data["method"],
            request_type=RequestType(
                data.get(
                    "request_type",
                    RequestType.API.value,
                )
            ),
            description=data.get(
                "description",
            ),
            request_schema=(
                SchemaSerializer.from_dict(
                    data["request_schema"],
                )
                if data.get("request_schema")
                else None
            ),
            response_schema=(
                SchemaSerializer.from_dict(
                    data["response_schema"],
                )
                if data.get("response_schema")
                else None
            ),
        )

        endpoint.tags.update(
            data.get(
                "tags",
                [],
            )
        )

        endpoint.requests.extend(
            HttpRequestSerializer.from_dict(item)
            for item in data.get(
                "requests",
                [],
            )
        )

        endpoint.responses.extend(
            HttpResponseSerializer.from_dict(item)
            for item in data.get(
                "responses",
                [],
            )
        )

        return endpoint
