from __future__ import annotations

from collections.abc import Iterator

from jit.entities.api_endpoint import ApiEndpoint
from jit.entities.http_request import HttpRequest
from jit.entities.http_response import HttpResponse


class EndpointDetector:
    """
    Groups captured requests and responses into API endpoints.
    """

    def __init__(self) -> None:
        self._endpoints: dict[
            tuple[str, str],
            ApiEndpoint,
        ] = {}

    @staticmethod
    def _key(
        method: str,
        path: str,
    ) -> tuple[str, str]:
        """
        Normalize the lookup key.
        """

        return (
            method.upper(),
            path,
        )

    def add_request(
        self,
        request: HttpRequest,
    ) -> ApiEndpoint:
        """
        Add a captured request.

        Creates the endpoint if it does not already exist.
        """

        key = self._key(
            request.method,
            request.path,
        )

        endpoint = self._endpoints.get(key)

        if endpoint is None:
            endpoint = ApiEndpoint(
                path=request.path,
                method=request.method.upper(),
            )

            self._endpoints[key] = endpoint

        endpoint.add_request(request)

        return endpoint

    def add_response(
        self,
        response: HttpResponse,
    ) -> ApiEndpoint | None:
        """
        Attach a response to its endpoint.

        Responses are matched using the request_id.
        """

        for endpoint in self._endpoints.values():
            if any(
                request.id == response.request_id
                for request in endpoint.requests
            ):
                endpoint.add_response(response)
                return endpoint

        return None

    def get(
        self,
        method: str,
        path: str,
    ) -> ApiEndpoint | None:
        """
        Retrieve an endpoint.
        """

        return self._endpoints.get(
            self._key(
                method,
                path,
            )
        )

    def all(self) -> list[ApiEndpoint]:
        """
        Return all discovered endpoints.
        """

        return list(
            self._endpoints.values()
        )

    def clear(self) -> None:
        """
        Remove every discovered endpoint.
        """

        self._endpoints.clear()

    def __len__(self) -> int:
        return len(self._endpoints)

    def __iter__(self) -> Iterator[ApiEndpoint]:
        return iter(self._endpoints.values())
