from __future__ import annotations

from jit.entities.schema import Schema
from jit.entities.schema_field import SchemaField
from jit.inference.schema_merger import SchemaMerger


def test_merge_new_field() -> None:
    left = Schema()
    left.add_field(
        SchemaField(
            name="id",
            field_type="integer",
        )
    )

    right = Schema()
    right.add_field(
        SchemaField(
            name="price",
            field_type="number",
        )
    )

    merged = SchemaMerger.merge(
        left,
        right,
    )

    assert len(merged.fields) == 2

    assert merged.get_field("id") is not None
    assert merged.get_field("price") is not None


def test_merge_same_field() -> None:
    left = Schema()
    left.add_field(
        SchemaField(
            name="id",
            field_type="integer",
        )
    )

    right = Schema()
    right.add_field(
        SchemaField(
            name="id",
            field_type="integer",
        )
    )

    merged = SchemaMerger.merge(
        left,
        right,
    )

    assert len(merged.fields) == 1

    field = merged.get_field("id")

    assert field is not None
    assert field.field_type == "integer"


def test_merge_nested_objects() -> None:
    left = Schema()

    seller_left = SchemaField(
        name="seller",
        field_type="object",
    )

    seller_left.children.append(
        SchemaField(
            name="id",
            field_type="integer",
        )
    )

    left.add_field(seller_left)

    right = Schema()

    seller_right = SchemaField(
        name="seller",
        field_type="object",
    )

    seller_right.children.append(
        SchemaField(
            name="name",
            field_type="string",
        )
    )

    right.add_field(seller_right)

    merged = SchemaMerger.merge(
        left,
        right,
    )

    seller = merged.get_field("seller")

    assert seller is not None
    assert seller.field_type == "object"
    assert len(seller.children) == 2

    names = {child.name for child in seller.children}

    assert names == {
        "id",
        "name",
    }


def test_merge_array_objects() -> None:
    left = Schema()

    products_left = SchemaField(
        name="products",
        field_type="array",
    )

    products_left.children.append(
        SchemaField(
            name="id",
            field_type="integer",
        )
    )

    left.add_field(products_left)

    right = Schema()

    products_right = SchemaField(
        name="products",
        field_type="array",
    )

    products_right.children.append(
        SchemaField(
            name="price",
            field_type="number",
        )
    )

    right.add_field(products_right)

    merged = SchemaMerger.merge(
        left,
        right,
    )

    products = merged.get_field("products")

    assert products is not None
    assert products.field_type == "array"
    assert len(products.children) == 2

    names = {child.name for child in products.children}

    assert names == {
        "id",
        "price",
    }
