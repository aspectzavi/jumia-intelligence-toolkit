from __future__ import annotations

import yaml

from jit.exporters.yaml_exporter import YamlExporter


class DummyDocument:
    def to_dict(self) -> dict[str, object]:
        return {
            "name": "jit",
            "version": 1,
            "items": [1, 2, 3],
        }


def test_dumps_returns_valid_yaml() -> None:
    document = DummyDocument()

    text = YamlExporter.dumps(document)

    data = yaml.safe_load(text)

    assert data["name"] == "jit"
    assert data["version"] == 1
    assert data["items"] == [1, 2, 3]


def test_export(tmp_path) -> None:
    document = DummyDocument()

    output = tmp_path / "api.yaml"

    returned = YamlExporter.export(
        document,
        output,
    )

    assert returned == output
    assert output.exists()

    data = yaml.safe_load(
        output.read_text(
            encoding="utf-8",
        )
    )

    assert data["name"] == "jit"
    assert data["version"] == 1


def test_export_creates_parent_directory(tmp_path) -> None:
    document = DummyDocument()

    output = tmp_path / "nested" / "folder" / "api.yaml"

    YamlExporter.export(
        document,
        output,
    )

    assert output.exists()


def test_sort_keys() -> None:
    document = DummyDocument()

    text = YamlExporter.dumps(
        document,
        sort_keys=True,
    )

    data = yaml.safe_load(text)

    assert data["name"] == "jit"
    assert data["version"] == 1


def test_yaml_is_readable() -> None:
    document = DummyDocument()

    text = YamlExporter.dumps(document)

    assert "name:" in text
    assert "version:" in text
    assert "items:" in text
