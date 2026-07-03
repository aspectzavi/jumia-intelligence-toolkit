from __future__ import annotations

from jit.openapi.openapi_document import OpenApiDocument
from jit.openapi.openapi_path import OpenApiPath


def test_create_document():
    document = OpenApiDocument()

    assert document.title == "Discovered API"
    assert document.version == "1.0.0"
    assert len(document.paths) == 0


def test_add_path():
    document = OpenApiDocument()

    path = OpenApiPath()

    document.add_path("/products", path)

    assert document.get_path("/products") is path


def test_to_dict():
    document = OpenApiDocument()

    document.add_path(
        "/products",
        OpenApiPath(),
    )

    data = document.to_dict()

    assert data["openapi"] == "3.1.0"
    assert "/products" in data["paths"]
