from __future__ import annotations

from jit.inference.type_inferer import TypeInferer


def test_none() -> None:
    assert TypeInferer.infer(None) == "null"


def test_bool() -> None:
    assert TypeInferer.infer(True) == "boolean"


def test_integer() -> None:
    assert TypeInferer.infer(123) == "integer"


def test_float() -> None:
    assert TypeInferer.infer(12.5) == "number"


def test_string() -> None:
    assert TypeInferer.infer("hello") == "string"


def test_object() -> None:
    assert TypeInferer.infer({"id": 1}) == "object"


def test_array() -> None:
    assert TypeInferer.infer([1, 2, 3]) == "array"


def test_bytes() -> None:
    assert TypeInferer.infer(b"abc") == "bytes"
