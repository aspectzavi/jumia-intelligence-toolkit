from __future__ import annotations

from jit.openapi.openapi_document import OpenApiDocument
from jit.openapi.openapi_operation import OpenApiOperation
from jit.openapi.openapi_path import OpenApiPath
from jit.openapi.openapi_schema import OpenApiSchema


def create_document() -> OpenApiDocument:
    return OpenApiDocument(
        title="Test API",
        version="1.0.0",
    )


def test_create_document():
    document = create_document()

    assert document.title == "Test API"
    assert document.version == "1.0.0"
    assert len(document.paths) == 0


def test_add_path():
    document = create_document()

    path = OpenApiPath()

    document.add_path(
        "/products",
        path,
    )

    assert document.get_path("/products") is path
    assert len(document.paths) == 1


def test_replace_existing_path():
    document = create_document()

    path1 = OpenApiPath()
    path2 = OpenApiPath()

    document.add_path(
        "/products",
        path1,
    )

    document.add_path(
        "/products",
        path2,
    )

    assert document.get_path("/products") is path2
    assert len(document.paths) == 1


def test_to_dict():
    document = create_document()

    path = OpenApiPath()

    operation = OpenApiOperation(
        request_body=OpenApiSchema(type="object"),
    )

    path.add_operation(
        "GET",
        operation,
    )

    document.add_path(
        "/products",
        path,
    )

    data = document.to_dict()

    assert data["openapi"] == "3.1.0"
    assert data["info"]["title"] == "Test API"
    assert data["info"]["version"] == "1.0.0"
    assert "/products" in data["paths"]


def test_from_dict():
    original = create_document()

    path = OpenApiPath()

    operation = OpenApiOperation(
        request_body=OpenApiSchema(type="object"),
    )

    path.add_operation(
        "POST",
        operation,
    )

    original.add_path(
        "/login",
        path,
    )

    restored = OpenApiDocument.from_dict(
        original.to_dict(),
    )

    assert restored.title == original.title
    assert restored.version == original.version
    assert restored.get_path("/login") is not None


def test_iter():
    document = create_document()

    document.add_path(
        "/one",
        OpenApiPath(),
    )

    document.add_path(
        "/two",
        OpenApiPath(),
    )

    paths = list(document)

    assert len(paths) == 2


def test_len():
    document = create_document()

    assert len(document) == 0

    document.add_path(
        "/products",
        OpenApiPath(),
    )

    assert len(document) == 1


def test_str():
    document = create_document()

    document.add_path(
        "/products",
        OpenApiPath(),
    )

    text = str(document)

    assert "OpenApiDocument" in text
    assert "1 paths" in text
