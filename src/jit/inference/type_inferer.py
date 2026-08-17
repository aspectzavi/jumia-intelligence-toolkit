from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any


class TypeInferer:
    """
    Infers the schema type of a Python value.

    The returned type names are intentionally generic so they
    can be used across JSON Schema, OpenAPI, and internal JIT
    schema representations.
    """

    @staticmethod
    def infer(
        value: Any,
    ) -> str:
        """
        Infer the type of a Python value.
        """

        if value is None:
            return "null"

        # bool must be checked before int because
        # bool is a subclass of int.
        if isinstance(value, bool):
            return "boolean"

        if isinstance(value, int):
            return "integer"

        if isinstance(value, float):
            return "number"

        if isinstance(value, str):
            return "string"

        if isinstance(value, bytes):
            return "bytes"

        if isinstance(value, Mapping):
            return "object"

        if (
            isinstance(value, Sequence)
            and not isinstance(
                value,
                (
                    str,
                    bytes,
                    bytearray,
                ),
            )
        ):
            return "array"

        return "unknown"
