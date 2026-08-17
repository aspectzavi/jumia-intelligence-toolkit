from __future__ import annotations

import json

from jit.exporters.json_exporter import JsonExporter


class DummyDocument:
    def to_dict(self) -> dict[str, object]:
        return {
            "name": "jit",
            "version": 1,
            "items": [1, 2, 3],
        }


def test_dumps_returns_valid_json() -> None:
    document = DummyDocument()

    text = JsonExporter.dumps(document)

    data = json.loads(text)

    assert data["name"] == "jit"
    assert data["version"] == 1
    assert data["items"] == [1, 2, 3]


def test_dumps_with_sort_keys() -> None:
    document = DummyDocument()

    text = JsonExporter.dumps(
        document,
        sort_keys=True,
    )

    assert '"items"' in text
    assert '"name"' in text
    assert '"version"' in text


def test_export(tmp_path) -> None:
    document = DummyDocument()

    output = tmp_path / "api.json"

    returned = JsonExporter.export(
        document,
        output,
    )

    assert returned == output
    assert output.exists()

    data = json.loads(output.read_text(encoding="utf-8"))

    assert data["name"] == "jit"
    assert data["version"] == 1


def test_export_creates_parent_directory(tmp_path) -> None:
    document = DummyDocument()

    output = tmp_path / "nested" / "folder" / "api.json"

    JsonExporter.export(
        document,
        output,
    )

    assert output.exists()


def test_indent_option() -> None:
    document = DummyDocument()

    text = JsonExporter.dumps(
        document,
        indent=4,
    )

    assert "\n" in text
    assert "    " in text
