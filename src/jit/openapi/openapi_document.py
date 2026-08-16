from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import Any

from jit.openapi.openapi_path import OpenApiPath


@dataclass(slots=True)
class OpenApiDocument:
    """
    Represents a complete OpenAPI document.
    """

    title: str

    version: str

    openapi: str = "3.1.0"

    paths: dict[str, OpenApiPath] = field(
        default_factory=dict,
    )

    def add_path(
        self,
        path: str,
        openapi_path: OpenApiPath,
    ) -> None:
        """
        Add or replace a path.
        """

        self.paths[path] = openapi_path

    def get_path(
        self,
        path: str,
    ) -> OpenApiPath | None:
        """
        Retrieve a path.
        """

        return self.paths.get(path)

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize the document.
        """

        return {
            "openapi": self.openapi,
            "info": {
                "title": self.title,
                "version": self.version,
            },
            "paths": {
                path: value.to_dict()
                for path, value in self.paths.items()
            },
        }

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> OpenApiDocument:
        """
        Deserialize an OpenAPI document.
        """

        info = data.get("info", {})

        document = cls(
            title=info.get("title", ""),
            version=info.get("version", ""),
            openapi=data.get("openapi", "3.1.0"),
        )

        for path, value in data.get(
            "paths",
            {},
        ).items():
            document.add_path(
                path,
                OpenApiPath.from_dict(
                    path,
                    value,
                ),
            )

        return document

    def __len__(self) -> int:
        return len(self.paths)

    def __iter__(self) -> Iterator[OpenApiPath]:
        return iter(self.paths.values())

    def __contains__(
        self,
        path: str,
    ) -> bool:
        return path in self.paths

    def __str__(self) -> str:
        return (
            f"OpenApiDocument("
            f"{len(self.paths)} paths)"
        )
