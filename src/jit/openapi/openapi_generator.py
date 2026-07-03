from __future__ import annotations

from jit.discovery.api_mapper import ApiMapper
from jit.entities.schema import Schema
from jit.openapi.openapi_document import OpenApiDocument
from jit.openapi.openapi_operation import OpenApiOperation
from jit.openapi.openapi_path import OpenApiPath
from jit.openapi.openapi_schema import OpenApiSchema


class OpenApiGenerator:
    """
    Converts discovered API endpoints into an OpenAPI document.
    """

    @classmethod
    def generate(
        cls,
        mapper: ApiMapper,
        *,
        title: str = "Discovered API",
        version: str = "1.0.0",
    ) -> OpenApiDocument:

        document = OpenApiDocument(
            title=title,
            version=version,
        )

        for endpoint in mapper:

            path = document.get_path(endpoint.path)

            if path is None:
                path = OpenApiPath()
                document.add_path(
                    endpoint.path,
                    path,
                )

            operation = OpenApiOperation()

            if endpoint.request_schema is not None:
                operation.request_body = cls._schema_to_openapi(
                    endpoint.request_schema,
                )

            if endpoint.response_schema is not None:
                operation.responses[200] = cls._schema_to_openapi(
                    endpoint.response_schema,
                )

            path.add_operation(
                endpoint.method,
                operation,
            )

        return document

    @classmethod
    def _schema_to_openapi(
        cls,
        schema: Schema,
    ) -> OpenApiSchema:

        properties: dict[str, OpenApiSchema] = {}
        required: list[str] = []

        for field in schema:

            property_schema = OpenApiSchema(
                type=field.field_type,
            )

            if field.field_type == "object" and field.children:
                child = cls._schema_to_openapi(
                    Schema(fields=field.children),
                )

                property_schema.properties = child.properties
                property_schema.required = child.required

            properties[field.name] = property_schema

            if field.required:
                required.append(field.name)

        return OpenApiSchema(
            type="object",
            properties=properties,
            required=required,
        )
