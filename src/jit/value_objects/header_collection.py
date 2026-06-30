from __future__ import annotations

from collections.abc import Iterator
from typing import Any

from jit.entities.http_header import HttpHeader


class HeaderCollection:
    """
    Represents an ordered collection of HTTP headers.

    Header names are treated case-insensitively for lookups,
    while preserving their original casing.
    """

    def __init__(
        self,
        headers: list[HttpHeader] | None = None,
    ) -> None:
        self._headers: list[HttpHeader] = headers or []

    def __iter__(self) -> Iterator[HttpHeader]:
        return iter(self._headers)

    def __len__(self) -> int:
        return len(self._headers)

    def __contains__(self, name: str) -> bool:
        return self.has(name)

    def __getitem__(self, name: str) -> str:
        value = self.get(name)

        if value is None:
            raise KeyError(name)

        return value

    def __repr__(self) -> str:
        return (
            f"HeaderCollection({len(self._headers)} headers)"
        )

    @property
    def items(self) -> list[HttpHeader]:
        """
        Return all headers.
        """

        return self._headers

    @property
    def as_dict(self) -> dict[str, str]:
        """
        Return headers as a lowercase dictionary.
        """

        return {
            header.name.lower(): header.value
            for header in self._headers
        }

    def add(
        self,
        header: HttpHeader,
    ) -> None:
        """
        Add a header.
        """

        self._headers.append(header)

    def extend(
        self,
        headers: list[HttpHeader],
    ) -> None:
        """
        Add multiple headers.
        """

        self._headers.extend(headers)

    def get(
        self,
        name: str,
        default: str | None = None,
    ) -> str | None:
        """
        Return a header value.
        """

        return self.as_dict.get(
            name.lower(),
            default,
        )

    def get_all(
        self,
        name: str,
    ) -> list[str]:
        """
        Return all values for a header.
        """

        return [
            header.value
            for header in self._headers
            if header.name.lower() == name.lower()
        ]

    def has(
        self,
        name: str,
    ) -> bool:
        """
        Whether a header exists.
        """

        return self.get(name) is not None

    @property
    def content_type(self) -> str | None:
        return self.get("Content-Type")

    @property
    def content_length(self) -> int | None:
        value = self.get("Content-Length")

        if value is None:
            return None

        try:
            return int(value)
        except ValueError:
            return None

    @property
    def content_encoding(self) -> str | None:
        return self.get("Content-Encoding")

    @property
    def user_agent(self) -> str | None:
        return self.get("User-Agent")

    def to_dict(self) -> list[dict[str, Any]]:
        """
        Serialize the collection.
        """

        return [
            header.to_dict()
            for header in self._headers
        ]

    @classmethod
    def from_dict(
        cls,
        data: list[dict[str, Any]],
    ) -> HeaderCollection:
        """
        Deserialize a header collection.
        """

        return cls(
            [
                HttpHeader.from_dict(item)
                for item in data
            ]
        )
