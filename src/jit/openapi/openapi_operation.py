from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from jit.openapi.openapi_schema import OpenApiSchema


@dataclass(slots=True)
class OpenApiOperation:
    """
    Represents a single OpenAPI operation.
    """

    summary: str | None = None

    description: str | None = None

    request_body: OpenApiSchema | None = None

    responses: dict[int, OpenApiSchema] = field(
        default_factory=dict,
    )

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize the operation.
        """

        data: dict[str, Any] = {}

        if self.summary is not None:
            data["summary"] = self.summary

        if self.description is not None:
            data["description"] = self.description

        if self.request_body is not None:
            data["requestBody"] = {
                "content": {
                    "application/json": {
                        "schema": self.request_body.to_dict(),
                    }
                }
            }

        if self.responses:
            data["responses"] = {}

            for status, schema in self.responses.items():
                data["responses"][str(status)] = {
                    "description": "Successful response",
                    "content": {
                        "application/json": {
                            "schema": schema.to_dict(),
                        }
                    },
                }

        return data

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> OpenApiOperation:
        """
        Deserialize an operation.
        """

        operation = cls(
            summary=data.get("summary"),
            description=data.get("description"),
        )

        request_schema = (
            data.get("requestBody", {})
            .get("content", {})
            .get("application/json", {})
            .get("schema")
        )

        if request_schema is not None:
            operation.request_body = OpenApiSchema.from_dict(
                request_schema,
            )

        for status, response in data.get(
            "responses",
            {},
        ).items():

            schema = (
                response.get("content", {})
                .get("application/json", {})
                .get("schema")
            )

            if schema is not None:
                operation.responses[int(status)] = (
                    OpenApiSchema.from_dict(schema)
                )

        return operation

    def __str__(self) -> str:
        return (
            f"OpenApiOperation("
            f"{len(self.responses)} responses)"
        )
