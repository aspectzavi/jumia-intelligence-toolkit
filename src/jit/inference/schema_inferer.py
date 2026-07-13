from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from jit.entities.schema import Schema
from jit.entities.schema_field import SchemaField
from jit.inference.type_inferer import TypeInferer


class SchemaInferer:
    """
    Infers a Schema from a Python object.

    Supported payloads:

    - JSON objects
    - Nested objects
    - Arrays
    - Arrays of objects
    """

    @classmethod
    def infer(
        cls,
        payload: Mapping[str, Any],
    ) -> Schema:
        """
        Infer a Schema from a dictionary payload.
        """

        schema = Schema()

        for name, value in payload.items():
            schema.add_field(
                cls._infer_field(
                    name,
                    value,
                )
            )

        return schema

    @classmethod
    def _infer_field(
        cls,
        name: str,
        value: Any,
    ) -> SchemaField:
        """
        Infer a SchemaField.
        """

        field_type = TypeInferer.infer(value)

        field = SchemaField(
            name=name,
            field_type=field_type,
        )

        #
        # Nested object
        #
        if isinstance(value, Mapping):
            nested_schema = cls.infer(value)

            field.children.extend(
                nested_schema.fields,
            )

            return field

        #
        # Array
        #
        if isinstance(value, list):

            if not value:
                return field

            first = value[0]

            if isinstance(first, Mapping):

                nested_schema = cls.infer(first)

                field.children.extend(
                    nested_schema.fields,
                )

            return field

        return field
