from __future__ import annotations

from jit.discovery.schema_detector import SchemaDetector


def test_merge_adds_new_fields():
    first = SchemaDetector.detect(
        {
            "id": 1,
            "name": "Laptop",
        }
    )

    second = SchemaDetector.detect(
        {
            "id": 2,
            "price": 100,
        }
    )

    merged = SchemaDetector.merge(
        first,
        second,
    )

    assert len(merged) == 3

    assert merged.get_field("id") is not None
    assert merged.get_field("name") is not None
    assert merged.get_field("price") is not None


def test_merge_keeps_existing_type():
    first = SchemaDetector.detect(
        {
            "price": 100,
        }
    )

    second = SchemaDetector.detect(
        {
            "price": 200,
        }
    )

    merged = SchemaDetector.merge(
        first,
        second,
    )

    field = merged.get_field("price")

    assert field is not None
    assert field.field_type == "integer"


def test_merge_marks_optional_fields():
    first = SchemaDetector.detect(
        {
            "id": 1,
            "name": "Laptop",
        }
    )

    second = SchemaDetector.detect(
        {
            "id": 2,
        }
    )

    merged = SchemaDetector.merge(
        first,
        second,
    )

    id_field = merged.get_field("id")
    name_field = merged.get_field("name")

    assert id_field is not None
    assert id_field.required is True

    assert name_field is not None
    assert name_field.required is False
