from __future__ import annotations

from dataclasses import dataclass
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

    response_body: OpenApiSchema | None = None

    def to_dict(self) -> dict[str, Any]:
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

        if self.response_body is not None:
            data["responses"] = {
                "200": {
                    "description": "Successful response",
                    "content": {
                        "application/json": {
                            "schema": self.response_body.to_dict(),
                        }
                    },
                }
            }

        return data
