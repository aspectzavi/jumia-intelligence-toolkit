from __future__ import annotations

from jit.entities.schema_field import SchemaField


def test_create_schema_field():
    field = SchemaField(
        name="price",
        field_type="integer",
    )

    assert field.name == "price"
    assert field.field_type == "integer"
    assert field.required is True
    assert field.children == []


def test_add_child():
    parent = SchemaField(
        name="seller",
        field_type="object",
    )

    child = SchemaField(
        name="id",
        field_type="integer",
    )

    parent.add_child(child)

    assert len(parent.children) == 1
    assert parent.children[0] is child


def test_get_child():
    parent = SchemaField(
        name="seller",
        field_type="object",
    )

    child = SchemaField(
        name="name",
        field_type="string",
    )

    parent.add_child(child)

    assert parent.get_child("name") is child


def test_get_missing_child():
    parent = SchemaField(
        name="seller",
        field_type="object",
    )

    assert parent.get_child("missing") is None


def test_to_dict():
    field = SchemaField(
        name="price",
        field_type="integer",
    )

    assert field.to_dict() == {
        "name": "price",
        "field_type": "integer",
        "required": True,
        "children": [],
    }


def test_from_dict():
    field = SchemaField.from_dict(
        {
            "name": "price",
            "field_type": "integer",
            "required": False,
            "children": [],
        }
    )

    assert field.name == "price"
    assert field.field_type == "integer"
    assert field.required is False


def test_nested_from_dict():
    field = SchemaField.from_dict(
        {
            "name": "seller",
            "field_type": "object",
            "required": True,
            "children": [
                {
                    "name": "id",
                    "field_type": "integer",
                    "required": True,
                    "children": [],
                }
            ],
        }
    )

    assert len(field.children) == 1

    assert field.children[0].name == "id"

    assert field.children[0].field_type == "integer"


def test_string_representation():
    field = SchemaField(
        name="price",
        field_type="integer",
    )

    assert str(field) == "price: integer"
