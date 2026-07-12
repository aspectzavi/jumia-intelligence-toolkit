from __future__ import annotations

from jit.entities.schema import Schema
from jit.entities.schema_field import SchemaField


def test_create_empty_schema():
    schema = Schema()

    assert len(schema) == 0
    assert schema.fields == []


def test_add_field():
    schema = Schema()

    field = SchemaField(
        name="price",
        field_type="integer",
    )

    schema.add_field(field)

    assert len(schema) == 1
    assert schema.fields[0] is field


def test_get_existing_field():
    schema = Schema()

    field = SchemaField(
        name="price",
        field_type="integer",
    )

    schema.add_field(field)

    assert schema.get_field("price") is field


def test_get_missing_field():
    schema = Schema()

    assert schema.get_field("missing") is None


def test_duplicate_field_replaces_existing():
    schema = Schema()

    first = SchemaField(
        name="price",
        field_type="integer",
    )

    second = SchemaField(
        name="price",
        field_type="number",
    )

    schema.add_field(first)
    schema.add_field(second)

    assert len(schema) == 1
    assert schema.get_field("price") is second



def test_iter():
    schema = Schema()

    schema.add_field(
        SchemaField(
            name="id",
            field_type="integer",
        )
    )

    schema.add_field(
        SchemaField(
            name="name",
            field_type="string",
        )
    )

    names = [field.name for field in schema]

    assert names == [
        "id",
        "name",
    ]


def test_length():
    schema = Schema()

    schema.add_field(
        SchemaField(
            name="id",
            field_type="integer",
        )
    )

    schema.add_field(
        SchemaField(
            name="name",
            field_type="string",
        )
    )

    assert len(schema) == 2


def test_string_representation():
    schema = Schema()

    schema.add_field(
        SchemaField(
            name="id",
            field_type="integer",
        )
    )

    assert str(schema) == "Schema(1 fields)"
