from __future__ import annotations

from jit.entities.api_endpoint import ApiEndpoint
from jit.entities.http_response import HttpResponse
from jit.inference.schema_inferer import SchemaInferer
from jit.inference.schema_merger import SchemaMerger
from jit.parsers.response_parser import ResponseParser


class EndpointAnalyzer:
    """
    Enriches discovered API endpoints with additional intelligence.

    Responsibilities
    ----------------
    - Parse response bodies
    - Infer response schemas
    - Merge schemas from multiple responses
    - Record response examples
    - Track status codes
    - Track content types
    """

    def analyze(
        self,
        endpoint: ApiEndpoint,
    ) -> None:
        """
        Analyze every response belonging to an endpoint.
        """

        for response in endpoint.responses:
            self._analyze_response(
                endpoint,
                response,
            )

    def _analyze_response(
        self,
        endpoint: ApiEndpoint,
        response: HttpResponse,
    ) -> None:
        """
        Analyze a single HTTP response.
        """

        endpoint.add_status_code(
            response.status,
        )

        endpoint.add_content_type(
            response.content_type,
        )

        payload = ResponseParser.parse(
            response.body,
            response.content_type,
        )

        if payload is None:
            return

        endpoint.add_example(payload)

        #
        # Only infer schemas from JSON objects.
        #
        if not isinstance(payload, dict):
            return

        schema = SchemaInferer.infer(payload)

        if endpoint.response_schema is None:
            endpoint.response_schema = schema
        else:
            endpoint.response_schema = SchemaMerger.merge(
                endpoint.response_schema,
                schema,
            )

        endpoint.confidence = self._confidence(endpoint)

    @staticmethod
    def _confidence(
        endpoint: ApiEndpoint,
    ) -> float:
        """
        Very simple confidence estimate.

        This will become much smarter later.
        """

        count = endpoint.response_count

        if count == 0:
            return 0.0

        if count == 1:
            return 0.35

        if count < 5:
            return 0.60

        if count < 10:
            return 0.80

        return 1.0
