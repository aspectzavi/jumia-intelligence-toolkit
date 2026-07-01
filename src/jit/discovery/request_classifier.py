from __future__ import annotations

from jit.core.enums import RequestType
from jit.entities.http_request import HttpRequest


class RequestClassifier:
    """
    Classifies captured HTTP requests.
    """

    TRACKING_DOMAINS = (
        "google-analytics",
        "googletagmanager",
        "doubleclick",
        "facebook",
        "segment.io",
        "mixpanel",
        "hotjar",
        "clarity",
    )

    @classmethod
    def classify(
        cls,
        request: HttpRequest,
    ) -> RequestType:
        """
        Determine the request type.
        """

        url = request.url.lower()

        path = request.path.lower()

        resource = request.resource_type.lower()

        # Tracking endpoints take precedence over generic APIs.
        if any(
            domain in url
            for domain in cls.TRACKING_DOMAINS
        ):
            return RequestType.TRACKING

        if "/graphql" in path:
            return RequestType.GRAPHQL

        if request.is_api:
            return RequestType.API

        mapping = {
            "document": RequestType.DOCUMENT,
            "image": RequestType.IMAGE,
            "script": RequestType.SCRIPT,
            "stylesheet": RequestType.STYLESHEET,
            "font": RequestType.FONT,
            "media": RequestType.MEDIA,
        }

        return mapping.get(
            resource,
            RequestType.OTHER,
        )
