from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class OpenApiSchema:
    """
    Represents an OpenAPI schema object.
    """

    type: str | None = None

    properties: dict[str, "OpenApiSchema"] = field(
        default_factory=dict,
    )

    items: "OpenApiSchema | None" = None

    required: list[str] = field(
        default_factory=list,
    )

    description: str | None = None

    example: Any = None

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {}

        if self.type is not None:
            data["type"] = self.type

        if self.properties:
            data["properties"] = {
                name: schema.to_dict()
                for name, schema in self.properties.items()
            }

        if self.items is not None:
            data["items"] = self.items.to_dict()

        if self.required:
            data["required"] = self.required

        if self.description is not None:
            data["description"] = self.description

        if self.example is not None:
            data["example"] = self.example

        return data
