from __future__ import annotations

from jit.entities.schema_field import SchemaField
from jit.serializers.schema_field_serializer import (
    SchemaFieldSerializer,
)


def test_to_dict() -> None:
    field = SchemaField(
        name="id",
        field_type="integer",
    )

    result = SchemaFieldSerializer.to_dict(field)

    assert result["name"] == "id"
    assert result["field_type"] == "integer"
    assert result["required"] is True
    assert result["children"] == []


def test_from_dict() -> None:
    data = {
        "name": "email",
        "field_type": "string",
        "required": True,
        "children": [],
    }

    field = SchemaFieldSerializer.from_dict(data)

    assert field.name == "email"
    assert field.field_type == "string"
    assert field.required is True
    assert field.children == []


def test_round_trip() -> None:
    parent = SchemaField(
        name="user",
        field_type="object",
    )

    parent.add_child(
        SchemaField(
            name="id",
            field_type="integer",
        )
    )

    restored = SchemaFieldSerializer.from_dict(
        SchemaFieldSerializer.to_dict(parent)
    )

    assert restored.name == parent.name
    assert restored.field_type == parent.field_type
    assert restored.required == parent.required

    assert len(restored.children) == 1
    assert restored.children[0].name == "id"
    assert restored.children[0].field_type == "integer"
