from __future__ import annotations

from pathlib import Path
from typing import Any, Protocol, cast

import yaml


class SupportsToDict(Protocol):
    """
    Protocol for exportable objects.
    """

    def to_dict(self) -> dict[str, Any]:
        ...


class YamlExporter:
    """
    Exports objects to YAML.
    """

    @staticmethod
    def dumps(
        document: SupportsToDict,
        *,
        sort_keys: bool = False,
    ) -> str:
        """
        Serialize an object to YAML.
        """

        return cast(
            str,
            yaml.safe_dump(
                document.to_dict(),
                sort_keys=sort_keys,
                allow_unicode=True,
            ),
        )

    @classmethod
    def export(
        cls,
        document: SupportsToDict,
        path: str | Path,
        *,
        sort_keys: bool = False,
    ) -> Path:
        """
        Export an object to a YAML file.
        """

        output = Path(path)

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        output.write_text(
            cls.dumps(
                document,
                sort_keys=sort_keys,
            ),
            encoding="utf-8",
        )

        return output
