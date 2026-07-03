from __future__ import annotations

from collections.abc import Iterator
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
        Add or replace an HTTP operation.
        """

        self.operations[method.lower()] = operation

    def get_operation(
        self,
        method: str,
    ) -> OpenApiOperation | None:
        """
        Retrieve an operation.
        """

        return self.operations.get(method.lower())

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize the path.
        """

        return {
            method: operation.to_dict()
            for method, operation in self.operations.items()
        }

    @classmethod
    def from_dict(
        cls,
        path: str,
        data: dict[str, Any],
    ) -> OpenApiPath:
        """
        Deserialize a path item.
        """

        openapi_path = cls()

        for method, operation in data.items():
            openapi_path.add_operation(
                method,
                OpenApiOperation.from_dict(operation),
            )

        return openapi_path

    def __len__(self) -> int:
        return len(self.operations)

    def __iter__(self) -> Iterator[OpenApiOperation]:
        return iter(self.operations.values())

    def __str__(self) -> str:
        return (
            f"OpenApiPath({len(self.operations)} operations)"
        )
