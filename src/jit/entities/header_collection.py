from __future__ import annotations

from collections.abc import Iterator
from typing import Any

from jit.entities.http_header import HttpHeader


class HeaderCollection:
    """
    Represents an ordered collection of HTTP headers.

    Header names are treated case-insensitively.
    """

    def __init__(
        self,
        headers: list[HttpHeader] | None = None,
    ) -> None:
        self._headers: list[HttpHeader] = headers.copy() if headers else []
        self._cache: dict[str, str] = {}

        self._rebuild_cache()

    def _rebuild_cache(self) -> None:
        """
        Rebuild the internal lookup cache.
        """

        self._cache = {
            header.name: header.value
            for header in self._headers
        }

    def __iter__(self) -> Iterator[HttpHeader]:
        return iter(self._headers)

    def __len__(self) -> int:
        return len(self._headers)

    def __bool__(self) -> bool:
        return bool(self._headers)

    def __contains__(self, name: str) -> bool:
        return self.has(name)

    def __getitem__(self, name: str) -> str:
        value = self.get(name)

        if value is None:
            raise KeyError(name)

        return value

    def __eq__(
        self,
        other: object,
    ) -> bool:
        if not isinstance(other, HeaderCollection):
            return NotImplemented

        return self._headers == other._headers

    def __repr__(self) -> str:
        return (
            f"HeaderCollection({len(self)} headers)"
        )

    def __str__(self) -> str:
        return "\n".join(
            str(header)
            for header in self._headers
        )

    @property
    def items(self) -> list[HttpHeader]:
        """
        Return a copy of all headers.
        """

        return self._headers.copy()

    @property
    def as_dict(self) -> dict[str, str]:
        """
        Return headers as a dictionary.
        """

        return self._cache.copy()

    def add(
        self,
        header: HttpHeader,
    ) -> None:
        """
        Add a header.
        """

        self._headers.append(header)
        self._cache[header.name] = header.value

    def extend(
        self,
        headers: list[HttpHeader],
    ) -> None:
        """
        Add multiple headers.
        """

        self._headers.extend(headers)

        for header in headers:
            self._cache[header.name] = header.value

    def remove(
        self,
        name: str,
    ) -> None:
        """
        Remove all headers with the given name.
        """

        self._headers = [
            header
            for header in self._headers
            if not header.matches(name)
        ]

        self._rebuild_cache()

    def clear(self) -> None:
        """
        Remove all headers.
        """

        self._headers.clear()
        self._cache.clear()

    def copy(self) -> HeaderCollection:
        """
        Return a shallow copy.
        """

        return HeaderCollection(
            self._headers.copy()
        )

    def get(
        self,
        name: str,
        default: str | None = None,
    ) -> str | None:
        """
        Return the first matching header.
        """

        return self._cache.get(
            name.strip().lower(),
            default,
        )

    def get_all(
        self,
        name: str,
    ) -> list[str]:
        """
        Return all matching headers.
        """

        return [
            header.value
            for header in self._headers
            if header.matches(name)
        ]

    def has(
        self,
        name: str,
    ) -> bool:
        """
        Whether a header exists.
        """

        return name.strip().lower() in self._cache

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
        Deserialize a collection.
        """

        return cls(
            [
                HttpHeader.from_dict(item)
                for item in data
            ]
        )
