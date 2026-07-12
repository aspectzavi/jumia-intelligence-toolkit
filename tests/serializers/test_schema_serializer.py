from __future__ import annotations

from jit.entities.schema import Schema
from jit.entities.schema_field import SchemaField
from jit.serializers.schema_serializer import (
    SchemaSerializer,
)


def test_to_dict() -> None:
    schema = Schema()

    schema.add_field(
        SchemaField(
            name="id",
            field_type="integer",
        )
    )

    result = SchemaSerializer.to_dict(schema)

    assert len(result["fields"]) == 1
    assert result["fields"][0]["name"] == "id"
    assert result["fields"][0]["field_type"] == "integer"


def test_from_dict() -> None:
    data = {
        "fields": [
            {
                "name": "email",
                "field_type": "string",
                "required": True,
                "children": [],
            }
        ]
    }

    schema = SchemaSerializer.from_dict(data)

    assert len(schema.fields) == 1
    assert schema.fields[0].name == "email"
    assert schema.fields[0].field_type == "string"


def test_round_trip() -> None:
    schema = Schema()

    schema.add_field(
        SchemaField(
            name="user",
            field_type="object",
        )
    )

    serialized = SchemaSerializer.to_dict(schema)

    restored = SchemaSerializer.from_dict(serialized)

    assert SchemaSerializer.to_dict(restored) == serialized
