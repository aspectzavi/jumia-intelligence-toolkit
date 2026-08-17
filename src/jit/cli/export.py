from __future__ import annotations

from pathlib import Path
from typing import Protocol

from jit.exporters.json_exporter import JsonExporter
from jit.exporters.yaml_exporter import YamlExporter
from jit.openapi.openapi_document import OpenApiDocument


class SupportsExport(Protocol):
    """
    Protocol satisfied by JsonExporter and YamlExporter.
    """

    @classmethod
    def export(
        cls,
        document: OpenApiDocument,
        path: str | Path,
    ) -> Path:
        ...


EXPORTERS: dict[str, type[SupportsExport]] = {
    ".json": JsonExporter,
    ".yaml": YamlExporter,
    ".yml": YamlExporter,
}


class UnsupportedExportFormatError(ValueError):
    """
    Raised when the requested export path has an unsupported extension.
    """


def export_openapi(
    document: OpenApiDocument,
    path: str | Path,
) -> Path:
    """
    Export an OpenAPI document, selecting the serializer from the
    file extension.

    Supported extensions: .json, .yaml, .yml
    """

    output = Path(path)
    extension = output.suffix.lower()

    exporter = EXPORTERS.get(extension)

    if exporter is None:
        supported = ", ".join(sorted(EXPORTERS))
        raise UnsupportedExportFormatError(
            f"Unsupported export format '{extension}'. "
            f"Supported formats: {supported}"
        )

    return exporter.export(document, output)
