from __future__ import annotations

from collections.abc import Iterator

from jit.discovery.endpoint_detector import EndpointDetector
from jit.discovery.schema_detector import SchemaDetector
from jit.discovery.url_normalizer import URLNormalizer
from jit.entities.api_endpoint import ApiEndpoint
from jit.entities.http_request import HttpRequest
from jit.entities.http_response import HttpResponse


class ApiMapper:
    """
    High-level API discovery orchestrator.

    Coordinates endpoint detection and schema inference.
    """

    def __init__(self) -> None:
        self._detector = EndpointDetector()

    def add_request(
        self,
        request: HttpRequest,
    ) -> ApiEndpoint:
        """
        Add a captured request and infer its schema.
        """

        endpoint = self._detector.add_request(request)

        if isinstance(request.body, dict):
            schema = SchemaDetector.detect(request.body)

            if endpoint.request_schema is None:
                endpoint.request_schema = schema
            else:
                endpoint.request_schema = SchemaDetector.merge(
                    endpoint.request_schema,
                    schema,
                )

        return endpoint

    def add_response(
        self,
        response: HttpResponse,
    ) -> ApiEndpoint | None:
        """
        Attach a captured response and infer its schema.
        """

        endpoint = self._detector.add_response(response)

        if (
            endpoint is not None
            and isinstance(response.body, dict)
        ):
            schema = SchemaDetector.detect(response.body)

            if endpoint.response_schema is None:
                endpoint.response_schema = schema
            else:
                endpoint.response_schema = SchemaDetector.merge(
                    endpoint.response_schema,
                    schema,
                )

        return endpoint

    def add(
        self,
        request: HttpRequest,
        response: HttpResponse | None = None,
    ) -> ApiEndpoint:
        """
        Add a request and optionally its response.

        This convenience method supports synchronous discovery while
        internally delegating to add_request() and add_response().
        """

        endpoint = self.add_request(request)

        if response is not None:
            self.add_response(response)

        return endpoint

    def get(
        self,
        method: str,
        path: str,
    ) -> ApiEndpoint | None:
        """
        Retrieve an endpoint.

        The supplied path may be either:

        - a relative API path
        - a full URL

        The path is normalized before lookup.
        """

        normalized_path = URLNormalizer.normalize(path)

        return self._detector.get(
            method,
            normalized_path,
        )

    @property
    def endpoints(self) -> list[ApiEndpoint]:
        """
        Return all discovered endpoints.
        """

        return self._detector.all()

    def clear(self) -> None:
        """
        Remove every discovered endpoint.
        """

        self._detector.clear()

    def __len__(self) -> int:
        return len(self._detector)

    def __iter__(self) -> Iterator[ApiEndpoint]:
        return iter(self._detector)

    def __str__(self) -> str:
        return f"ApiMapper({len(self)} endpoints)"
