from __future__ import annotations

from typing import Any

from jit.entities.schema import Schema
from jit.serializers.schema_field_serializer import (
    SchemaFieldSerializer,
)


class SchemaSerializer:
    """
    Serializes Schema entities.
    """

    @staticmethod
    def to_dict(
        schema: Schema,
    ) -> dict[str, Any]:
        """
        Convert a Schema into a dictionary.
        """

        return {
            "fields": [
                SchemaFieldSerializer.to_dict(field)
                for field in schema.fields
            ]
        }

    @staticmethod
    def from_dict(
        data: dict[str, Any],
    ) -> Schema:
        """
        Create a Schema from a dictionary.
        """

        schema = Schema()

        for item in data.get(
            "fields",
            [],
        ):
            schema.add_field(
                SchemaFieldSerializer.from_dict(item)
            )

        return schema
