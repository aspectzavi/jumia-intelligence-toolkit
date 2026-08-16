from __future__ import annotations

from pathlib import Path

from jit.cli.export import UnsupportedExportFormatError, export_openapi
from jit.openapi.openapi_document import OpenApiDocument


def test_export_openapi_json(tmp_path: Path) -> None:
    document = OpenApiDocument(title="Test API", version="1.0.0")

    output = export_openapi(document, tmp_path / "api.json")

    assert output.exists()
    assert output.suffix == ".json"


def test_export_openapi_yaml(tmp_path: Path) -> None:
    document = OpenApiDocument(title="Test API", version="1.0.0")

    output = export_openapi(document, tmp_path / "api.yaml")

    assert output.exists()
    assert output.suffix == ".yaml"


def test_export_openapi_rejects_unsupported_extension(tmp_path: Path) -> None:
    document = OpenApiDocument(title="Test API", version="1.0.0")

    try:
        export_openapi(document, tmp_path / "api.txt")
        raised = False
    except UnsupportedExportFormatError:
        raised = True

    assert raised
