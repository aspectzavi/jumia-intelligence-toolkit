from __future__ import annotations

from jit.entities.schema import Schema
from jit.entities.schema_field import SchemaField


class SchemaMerger:
    """
    Merges two schemas into a single schema.
    """

    @classmethod
    def merge(
        cls,
        left: Schema,
        right: Schema,
    ) -> Schema:
        """
        Merge two schemas.

        Fields that exist in only one schema become optional.
        """

        merged = Schema()

        right_names = {
            field.name
            for field in right
        }

        #
        # Copy fields from the left schema.
        #
        for field in left:
            copy = cls._copy_field(field)

            if field.name not in right_names:
                copy.required = False

            merged.add_field(copy)

        #
        # Merge fields from the right schema.
        #
        for field in right:
            existing = merged.get_field(field.name)

            #
            # Field exists only in the right schema.
            #
            if existing is None:
                copy = cls._copy_field(field)
                copy.required = False
                merged.add_field(copy)
                continue

            cls._merge_field(
                existing,
                field,
            )

        return merged

    @classmethod
    def _merge_field(
        cls,
        target: SchemaField,
        source: SchemaField,
    ) -> None:
        """
        Merge one field into another.
        """

        #
        # A field is only required if it is required
        # in both schemas.
        #
        target.required = (
            target.required
            and source.required
        )

        #
        # Merge nested object/array children.
        #
        if (
            target.field_type in ("object", "array")
            and target.field_type == source.field_type
        ):
            source_children = {
                child.name: child
                for child in source.children
            }

            target_children = {
                child.name: child
                for child in target.children
            }

            #
            # Existing children
            #
            for name, target_child in target_children.items():
                source_child = source_children.get(name)

                if source_child is None:
                    target_child.required = False
                    continue

                cls._merge_field(
                    target_child,
                    source_child,
                )

            #
            # New children
            #
            for name, source_child in source_children.items():
                if name not in target_children:
                    copy = cls._copy_field(source_child)
                    copy.required = False
                    target.children.append(copy)

    @classmethod
    def _copy_field(
        cls,
        field: SchemaField,
    ) -> SchemaField:
        """
        Deep-copy a SchemaField.
        """

        copy = SchemaField(
            name=field.name,
            field_type=field.field_type,
            required=field.required,
        )

        copy.children.extend(
            cls._copy_field(child)
            for child in field.children
        )

        return copy
