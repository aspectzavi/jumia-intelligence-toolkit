from __future__ import annotations

from typing import Any

from jit.entities.schema import Schema
from jit.entities.schema_field import SchemaField


class SchemaDetector:
    """
    Infers a Schema from JSON-like data.
    """

    @classmethod
    def detect(
        cls,
        data: Any,
    ) -> Schema:
        """
        Build a Schema from a dictionary.
        """

        schema = Schema()

        if not isinstance(data, dict):
            return schema

        for name, value in data.items():
            schema.add_field(
                cls._detect_field(
                    name,
                    value,
                )
            )

        return schema

    @classmethod
    def _detect_field(
        cls,
        name: str,
        value: Any,
    ) -> SchemaField:
        """
        Infer a SchemaField from a value.
        """

        if value is None:
            return SchemaField(
                name=name,
                field_type="null",
            )

        if isinstance(value, bool):
            return SchemaField(
                name=name,
                field_type="boolean",
            )

        if isinstance(value, int):
            return SchemaField(
                name=name,
                field_type="integer",
            )

        if isinstance(value, float):
            return SchemaField(
                name=name,
                field_type="number",
            )

        if isinstance(value, str):
            return SchemaField(
                name=name,
                field_type="string",
            )

        if isinstance(value, dict):
            field = SchemaField(
                name=name,
                field_type="object",
            )

            nested = cls.detect(value)

            for child in nested:
                field.add_child(child)

            return field

        if isinstance(value, list):
            field = SchemaField(
                name=name,
                field_type="array",
            )

            if value:
                child = cls._detect_field(
                    "item",
                    value[0],
                )
                field.add_child(child)

            return field

        return SchemaField(
            name=name,
            field_type="unknown",
        )

    @classmethod
    def merge(
        cls,
        left: Schema,
        right: Schema,
    ) -> Schema:
        """
        Merge two schemas into one.

        Fields present in only one schema become optional.
        Existing field definitions are preserved.
        """

        merged = Schema()

        left_fields = {
            field.name: field
            for field in left
        }

        right_fields = {
            field.name: field
            for field in right
        }

        all_names = (
            left_fields.keys()
            | right_fields.keys()
        )

        for name in sorted(all_names):

            if name in left_fields and name in right_fields:

                field = left_fields[name]

                field.required = (
                    left_fields[name].required
                    and right_fields[name].required
                )

                merged.add_field(field)

            elif name in left_fields:

                field = left_fields[name]
                field.required = False
                merged.add_field(field)

            else:

                field = right_fields[name]
                field.required = False
                merged.add_field(field)

        return merged
