from __future__ import annotations

from enum import StrEnum


class RequestType(StrEnum):
    """
    Classification of captured requests.
    """

    API = "api"
    GRAPHQL = "graphql"

    DOCUMENT = "document"

    IMAGE = "image"

    SCRIPT = "script"

    STYLESHEET = "stylesheet"

    FONT = "font"

    MEDIA = "media"

    TRACKING = "tracking"

    OTHER = "other"
