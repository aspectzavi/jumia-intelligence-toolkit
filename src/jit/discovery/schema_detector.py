from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from jit.entities.schema import Schema
from jit.entities.schema_field import SchemaField
from jit.inference.schema_inferer import SchemaInferer
from jit.inference.schema_merger import SchemaMerger
from jit.inference.type_inferer import TypeInferer


class SchemaDetector:
    """
    Compatibility wrapper for schema inference.

    This class preserves the original discovery-layer schema
    representation while delegating inference to the newer
    inference package.
    """

    @classmethod
    def detect(
        cls,
        data: Any,
    ) -> Schema:
        """
        Infer a Schema from arbitrary JSON-like data.
        """

        if not isinstance(data, Mapping):
            return Schema()

        schema = SchemaInferer.infer(data)

        cls._convert_schema(
            schema,
            data,
        )

        return schema

    @classmethod
    def merge(
        cls,
        left: Schema,
        right: Schema,
    ) -> Schema:
        """
        Merge two schemas into one.
        """

        return SchemaMerger.merge(
            left,
            right,
        )

    @classmethod
    def _convert_schema(
        cls,
        schema: Schema,
        payload: Mapping[str, Any],
    ) -> None:
        """
        Convert inferred schemas into the legacy discovery format.
        """

        for field in schema:
            cls._convert_field(
                field,
                payload.get(field.name),
            )

    @classmethod
    def _convert_field(
        cls,
        field: SchemaField,
        value: Any,
    ) -> None:
        """
        Recursively convert array/object fields.
        """

        #
        # Arrays
        #
        if field.field_type == "array":

            #
            # Primitive array.
            #
            if not field.children:

                item_type = "unknown"

                if (
                    isinstance(value, list)
                    and value
                ):
                    item_type = TypeInferer.infer(
                        value[0],
                    )

                field.children.append(
                    SchemaField(
                        name="item",
                        field_type=item_type,
                    )
                )

                return

            #
            # Already wrapped.
            #
            if (
                len(field.children) == 1
                and field.children[0].name == "item"
            ):
                child_value = None

                if (
                    isinstance(value, list)
                    and value
                ):
                    child_value = value[0]

                cls._convert_field(
                    field.children[0],
                    child_value,
                )

                return

            #
            # Wrap array-of-object fields.
            #
            item = SchemaField(
                name="item",
                field_type="object",
            )

            item.children.extend(field.children)

            field.children = [item]

            child_value = None

            if (
                isinstance(value, list)
                and value
            ):
                child_value = value[0]

            cls._convert_field(
                item,
                child_value,
            )

            return

        #
        # Objects
        #
        if field.field_type == "object":

            mapping = value if isinstance(value, Mapping) else {}

            for child in field.children:
                cls._convert_field(
                    child,
                    mapping.get(child.name),
                )

            return

        #
        # Primitive fields require no conversion.
        #
        return
