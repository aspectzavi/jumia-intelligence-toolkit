from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import Any

from jit.entities.schema_field import SchemaField


@dataclass(slots=True)
class Schema:
    """
    Represents an inferred API schema.
    """

    fields: list[SchemaField] = field(
        default_factory=list,
    )

    def add_field(
        self,
        schema_field: SchemaField,
    ) -> None:
        """
        Add or replace a field.
        """

        existing = self.get_field(schema_field.name)

        if existing is not None:
            index = self.fields.index(existing)
            self.fields[index] = schema_field
            return

        self.fields.append(schema_field)

    def get_field(
        self,
        name: str,
    ) -> SchemaField | None:
        """
        Return a field by name.
        """

        for schema_field in self.fields:
            if schema_field.name == name:
                return schema_field

        return None

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize the schema.
        """

        return {
            "fields": [
                schema_field.to_dict()
                for schema_field in self.fields
            ]
        }

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> Schema:
        """
        Deserialize a schema.
        """

        schema = cls()

        schema.fields.extend(
            SchemaField.from_dict(item)
            for item in data.get(
                "fields",
                [],
            )
        )

        return schema

    def __iter__(self) -> Iterator[SchemaField]:
        """
        Iterate over fields.
        """

        return iter(self.fields)

    def __len__(self) -> int:
        """
        Number of fields.
        """

        return len(self.fields)

    def __str__(self) -> str:
        return f"Schema({len(self)} fields)"
