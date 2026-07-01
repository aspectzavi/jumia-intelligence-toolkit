from __future__ import annotations

from jit.discovery.schema_detector import SchemaDetector


def test_empty_object():
    schema = SchemaDetector.detect({})

    assert len(schema) == 0


def test_detect_string():
    schema = SchemaDetector.detect(
        {
            "name": "Laptop",
        }
    )

    field = schema.get_field("name")

    assert field is not None
    assert field.field_type == "string"


def test_detect_integer():
    schema = SchemaDetector.detect(
        {
            "price": 100,
        }
    )

    field = schema.get_field("price")

    assert field is not None
    assert field.field_type == "integer"


def test_detect_float():
    schema = SchemaDetector.detect(
        {
            "rating": 4.5,
        }
    )

    field = schema.get_field("rating")

    assert field is not None
    assert field.field_type == "number"


def test_detect_boolean():
    schema = SchemaDetector.detect(
        {
            "active": True,
        }
    )

    field = schema.get_field("active")

    assert field is not None
    assert field.field_type == "boolean"


def test_detect_null():
    schema = SchemaDetector.detect(
        {
            "image": None,
        }
    )

    field = schema.get_field("image")

    assert field is not None
    assert field.field_type == "null"


def test_detect_nested_object():
    schema = SchemaDetector.detect(
        {
            "seller": {
                "id": 1,
                "name": "Jumia",
            }
        }
    )

    seller = schema.get_field("seller")

    assert seller is not None
    assert seller.field_type == "object"

    child_id = seller.get_child("id")
    assert child_id is not None
    assert child_id.field_type == "integer"

    child_name = seller.get_child("name")
    assert child_name is not None
    assert child_name.field_type == "string"


def test_detect_string_array():
    schema = SchemaDetector.detect(
        {
            "tags": [
                "electronics",
                "phones",
            ]
        }
    )

    tags = schema.get_field("tags")

    assert tags is not None
    assert tags.field_type == "array"

    assert len(tags.children) == 1

    assert tags.children[0].field_type == "string"


def test_detect_array_of_objects():
    schema = SchemaDetector.detect(
        {
            "products": [
                {
                    "id": 1,
                    "name": "Laptop",
                    "price": 100,
                }
            ]
        }
    )

    products = schema.get_field("products")

    assert products is not None
    assert products.field_type == "array"

    assert len(products.children) == 1

    item = products.children[0]

    assert item.field_type == "object"

    child_id = item.get_child("id")
    assert child_id is not None
    assert child_id.field_type == "integer"

    child_name = item.get_child("name")
    assert child_name is not None
    assert child_name.field_type == "string"

    child_price = item.get_child("price")
    assert child_price is not None
    assert child_price.field_type == "integer"


def test_detect_nested_array():
    schema = SchemaDetector.detect(
        {
            "seller": {
                "products": [
                    {
                        "id": 1,
                    }
                ]
            }
        }
    )

    seller = schema.get_field("seller")
    assert seller is not None

    products = seller.get_child("products")
    assert products is not None
    assert products.field_type == "array"

    item = products.children[0]

    child = item.get_child("id")
    assert child is not None
    assert child.field_type == "integer"
