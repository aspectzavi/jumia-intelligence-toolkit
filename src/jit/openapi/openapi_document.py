from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from jit.openapi.openapi_path import OpenApiPath


@dataclass(slots=True)
class OpenApiDocument:
    """
    Represents an OpenAPI 3.1 document.
    """

    title: str = "Discovered API"

    version: str = "1.0.0"

    openapi: str = "3.1.0"

    paths: dict[str, OpenApiPath] = field(
        default_factory=dict,
    )

    def add_path(
        self,
        path: str,
        item: OpenApiPath,
    ) -> None:
        """
        Add or replace a path item.
        """

        self.paths[path] = item

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
        Serialize the OpenAPI document.
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

        document = cls(
            title=data["info"]["title"],
            version=data["info"]["version"],
            openapi=data.get(
                "openapi",
                "3.1.0",
            ),
        )

        for path, value in data.get(
            "paths",
            {},
        ).items():
            document.paths[path] = OpenApiPath.from_dict(
                path,
                value,
            )

        return document

    def __len__(self) -> int:
        return len(self.paths)

    def __str__(self) -> str:
        return (
            f"OpenApiDocument("
            f"{len(self.paths)} paths)"
        )
