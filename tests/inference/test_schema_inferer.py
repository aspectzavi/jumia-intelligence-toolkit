from __future__ import annotations

from jit.inference.schema_inferer import SchemaInferer


def test_empty_object() -> None:
    schema = SchemaInferer.infer({})

    assert len(schema.fields) == 0


def test_simple_fields() -> None:
    schema = SchemaInferer.infer(
        {
            "id": 1,
            "name": "Phone",
            "price": 99.5,
            "active": True,
        }
    )

    assert schema.get_field("id").field_type == "integer"
    assert schema.get_field("name").field_type == "string"
    assert schema.get_field("price").field_type == "number"
    assert schema.get_field("active").field_type == "boolean"


def test_nested_object() -> None:
    schema = SchemaInferer.infer(
        {
            "seller": {
                "id": 5,
                "name": "Samsung",
            }
        }
    )

    seller = schema.get_field("seller")

    assert seller is not None
    assert seller.field_type == "object"
    assert len(seller.children) == 2


def test_array() -> None:
    schema = SchemaInferer.infer(
        {
            "images": [
                "a.jpg",
                "b.jpg",
            ]
        }
    )

    images = schema.get_field("images")

    assert images is not None
    assert images.field_type == "array"


def test_array_of_objects() -> None:
    schema = SchemaInferer.infer(
        {
            "products": [
                {
                    "id": 1,
                    "name": "TV",
                }
            ]
        }
    )

    products = schema.get_field("products")

    assert products is not None
    assert products.field_type == "array"
    assert len(products.children) == 2
