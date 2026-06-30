from __future__ import annotations

from abc import ABC
from dataclasses import dataclass, field
from typing import Any

from jit.core.base_entity import BaseEntity
from jit.entities.http_header import HttpHeader


@dataclass(slots=True)
class BaseHttpMessage(BaseEntity, ABC):
    """
    Base class shared by every HTTP message.

    Provides common header utilities.
    """

    headers: list[HttpHeader] = field(
        default_factory=list
    )

    @property
    def header_map(self) -> dict[str, str]:
        """
        Return headers as a lowercase dictionary.
        """

        return {
            header.name.lower(): header.value
            for header in self.headers
        }

    def get_header(
        self,
        name: str,
    ) -> str | None:
        """
        Return a header value.
        """

        return self.header_map.get(
            name.lower()
        )

    def has_header(
        self,
        name: str,
    ) -> bool:
        """
        Whether a header exists.
        """

        return (
            self.get_header(name)
            is not None
        )

    def add_header(
        self,
        header: HttpHeader,
    ) -> None:
        """
        Append a header.
        """

        self.headers.append(header)

    @property
    def content_type(self) -> str | None:
        return self.get_header(
            "Content-Type"
        )

    @property
    def content_encoding(self) -> str | None:
        return self.get_header(
            "Content-Encoding"
        )

    @property
    def user_agent(self) -> str | None:
        return self.get_header(
            "User-Agent"
        )

    @property
    def content_length(self) -> int | None:

        value = self.get_header(
            "Content-Length"
        )

        if value is None:
            return None

        try:
            return int(value)

        except ValueError:
            return None

    def serialize_headers(
        self,
    ) -> list[dict[str, Any]]:
        """
        Serialize headers.
        """

        return [
            header.to_dict()
            for header in self.headers
        ]
