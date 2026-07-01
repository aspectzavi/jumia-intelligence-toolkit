from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from jit.openapi.openapi_operation import OpenApiOperation


@dataclass(slots=True)
class OpenApiPath:
    """
    Represents an OpenAPI path item.
    """

    operations: dict[str, OpenApiOperation] = field(
        default_factory=dict,
    )

    def add_operation(
        self,
        method: str,
        operation: OpenApiOperation,
    ) -> None:
        """
        Add an HTTP operation.
        """

        self.operations[
            method.lower()
        ] = operation

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize the path.
        """

        return {
            method: operation.to_dict()
            for method, operation in self.operations.items()
        }
