from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from jit.entities.header_collection import HeaderCollection
from jit.entities.http_header import HttpHeader


class HeaderAdapter:
    """
    Converts between various header representations and
    HeaderCollection.

    This adapter intentionally has no dependency on Playwright.
    """

    @staticmethod
    def empty() -> HeaderCollection:
        """
        Create an empty header collection.
        """

        return HeaderCollection()

    @staticmethod
    def from_mapping(
        headers: Mapping[str, str] | None,
    ) -> HeaderCollection:
        """
        Convert a mapping of headers into a HeaderCollection.

        Example:
            {
                "content-type": "application/json",
                "accept": "*/*",
            }
        """

        collection = HeaderCollection()

        if not headers:
            return collection

        for name, value in headers.items():
            collection.add(
                HttpHeader(
                    name=name,
                    value=value,
                )
            )

        return collection

    @staticmethod
    def from_pairs(
        headers: list[tuple[str, str]] | None,
    ) -> HeaderCollection:
        """
        Convert a list of (name, value) pairs into
        a HeaderCollection.
        """

        collection = HeaderCollection()

        if not headers:
            return collection

        for name, value in headers:
            collection.add(
                HttpHeader(
                    name=name,
                    value=value,
                )
            )

        return collection

    @staticmethod
    def to_mapping(
        headers: HeaderCollection,
    ) -> dict[str, str]:
        """
        Convert a HeaderCollection into a dictionary.

        Header names remain normalized because HttpHeader
        performs normalization internally.
        """

        return {header.name: header.value for header in headers}

    @staticmethod
    def to_pairs(
        headers: HeaderCollection,
    ) -> list[tuple[str, str]]:
        """
        Convert a HeaderCollection into a list of
        (name, value) tuples.
        """

        return [
            (
                header.name,
                header.value,
            )
            for header in headers
        ]

    @staticmethod
    def clone(
        headers: HeaderCollection,
    ) -> HeaderCollection:
        """
        Create a deep copy of a HeaderCollection.
        """

        return HeaderCollection(
            [
                HttpHeader(
                    name=header.name,
                    value=header.value,
                )
                for header in headers
            ]
        )

    @staticmethod
    def serialize(
        headers: HeaderCollection,
    ) -> list[dict[str, Any]]:
        """
        Serialize a HeaderCollection.
        """

        return headers.to_dict()

    @staticmethod
    def deserialize(
        data: list[dict[str, Any]],
    ) -> HeaderCollection:
        """
        Deserialize a HeaderCollection.
        """

        return HeaderCollection.from_dict(data)
