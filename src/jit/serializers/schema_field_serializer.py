from __future__ import annotations

from typing import Any

from jit.entities.schema_field import SchemaField


class SchemaFieldSerializer:
    """
    Serializes SchemaField entities.
    """

    @staticmethod
    def to_dict(
        field: SchemaField,
    ) -> dict[str, Any]:
        """
        Convert a SchemaField into a dictionary.
        """

        return {
            "name": field.name,
            "field_type": field.field_type,
            "required": field.required,
            "children": [
                SchemaFieldSerializer.to_dict(child)
                for child in field.children
            ],
        }

    @staticmethod
    def from_dict(
        data: dict[str, Any],
    ) -> SchemaField:
        """
        Create a SchemaField from a dictionary.
        """

        field = SchemaField(
            name=data["name"],
            field_type=data["field_type"],
            required=data.get(
                "required",
                True,
            ),
        )

        for child in data.get(
            "children",
            [],
        ):
            field.add_child(
                SchemaFieldSerializer.from_dict(child)
            )

        return field
