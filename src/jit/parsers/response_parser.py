from __future__ import annotations

import json
from typing import Any


class ResponseParser:
    """
    Parses HTTP response bodies.

    Supports:

    - JSON
    - Text
    - HTML
    - Binary detection

    The parser never raises parsing exceptions. Instead,
    it returns None when parsing is not possible.
    """

    JSON_TYPES = (
        "application/json",
        "application/ld+json",
        "application/problem+json",
    )

    TEXT_TYPES = (
        "text/plain",
        "text/html",
        "application/xml",
        "text/xml",
    )

    @classmethod
    def parse(
        cls,
        body: bytes | bytearray | memoryview | str | None,
        content_type: str | None,
    ) -> Any:
        """
        Parse a response body into a Python object.

        Returns
        -------
        dict
        list
        str
        bytes
        None
        """

        if body is None:
            return None

        content_type = (content_type or "").lower()

        #
        # Decode bytes if needed.
        #
        text: str
        if isinstance(body, (bytes, bytearray, memoryview)):
            try:
                text = bytes(body).decode("utf-8")
            except UnicodeDecodeError:
                return bytes(body)
        else:
            text = body

        #
        # JSON
        #
        if any(
            value in content_type
            for value in cls.JSON_TYPES
        ):
            return cls.parse_json(text)

        #
        # HTML / XML / TEXT
        #
        if any(
            value in content_type
            for value in cls.TEXT_TYPES
        ):
            return text

        #
        # Unknown content type.
        # Try JSON first.
        #
        parsed = cls.parse_json(text)

        if parsed is not None:
            return parsed

        return text

    @staticmethod
    def parse_json(
        text: str,
    ) -> dict[str, Any] | list[Any] | None:
        """
        Parse JSON.

        Returns None if decoding fails.
        """

        try:
            parsed: dict[str, Any] | list[Any] = json.loads(text)
            return parsed

        except (
            json.JSONDecodeError,
            TypeError,
        ):
            return None

    @staticmethod
    def is_json(
        content_type: str | None,
    ) -> bool:
        """
        Return whether the content type is JSON.
        """

        if content_type is None:
            return False

        content_type = content_type.lower()

        return "json" in content_type

    @staticmethod
    def is_html(
        content_type: str | None,
    ) -> bool:
        """
        Return whether the content type is HTML.
        """

        if content_type is None:
            return False

        return "text/html" in content_type.lower()

    @staticmethod
    def is_text(
        content_type: str | None,
    ) -> bool:
        """
        Return whether the content type is textual.
        """

        if content_type is None:
            return False

        content_type = content_type.lower()

        return (
            "text/" in content_type
            or "json" in content_type
            or "xml" in content_type
        )

    @staticmethod
    def is_binary(
        content_type: str | None,
    ) -> bool:
        """
        Return whether the content type is likely binary.
        """

        return not ResponseParser.is_text(content_type)
