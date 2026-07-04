from __future__ import annotations

from jit.discovery.schema_detector import SchemaDetector
from jit.entities.api_endpoint import ApiEndpoint


class SchemaManager:
    """
    Handles schema inference and merging for API endpoints.
    """

    @staticmethod
    def update_request_schema(
        endpoint: ApiEndpoint,
        body: object,
    ) -> None:
        """
        Infer and merge a request schema.
        """

        if not isinstance(body, dict):
            return

        schema = SchemaDetector.detect(body)

        if endpoint.request_schema is None:
            endpoint.request_schema = schema
        else:
            endpoint.request_schema = SchemaDetector.merge(
                endpoint.request_schema,
                schema,
            )

    @staticmethod
    def update_response_schema(
        endpoint: ApiEndpoint,
        body: object,
    ) -> None:
        """
        Infer and merge a response schema.
        """

        if not isinstance(body, dict):
            return

        schema = SchemaDetector.detect(body)

        if endpoint.response_schema is None:
            endpoint.response_schema = schema
        else:
            endpoint.response_schema = SchemaDetector.merge(
                endpoint.response_schema,
                schema,
            )
