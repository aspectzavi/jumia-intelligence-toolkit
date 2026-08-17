from __future__ import annotations

from jit.discovery.api_mapper import ApiMapper
from jit.openapi.openapi_document import OpenApiDocument
from jit.openapi.openapi_generator import OpenApiGenerator


def generate(
    mapper: ApiMapper,
    *,
    title: str = "Discovered API",
    version: str = "1.0.0",
) -> OpenApiDocument:
    """
    Generate an OpenAPI document from discovered endpoints.
    """

    return OpenApiGenerator.generate(
        mapper,
        title=title,
        version=version,
    )
