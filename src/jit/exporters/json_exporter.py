from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Protocol


class SupportsToDict(Protocol):
    """
    Protocol for exportable objects.
    """

    def to_dict(self) -> dict[str, Any]:
        ...


class JsonExporter:
    """
    Exports objects to JSON.

    Any object implementing ``to_dict()`` is supported.
    """

    @staticmethod
    def dumps(
        document: SupportsToDict,
        *,
        indent: int = 2,
        sort_keys: bool = False,
    ) -> str:
        """
        Serialize an object to JSON.
        """

        return json.dumps(
            document.to_dict(),
            indent=indent,
            sort_keys=sort_keys,
            ensure_ascii=False,
        )

    @classmethod
    def export(
        cls,
        document: SupportsToDict,
        path: str | Path,
        *,
        indent: int = 2,
        sort_keys: bool = False,
    ) -> Path:
        """
        Export an object to a JSON file.
        """

        output = Path(path)

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        output.write_text(
            cls.dumps(
                document,
                indent=indent,
                sort_keys=sort_keys,
            ),
            encoding="utf-8",
        )

        return output
