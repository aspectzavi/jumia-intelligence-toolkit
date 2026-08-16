from __future__ import annotations

from jit.parsers.response_parser import ResponseParser


def test_parse_json_object() -> None:
    result = ResponseParser.parse(
        '{"id": 1, "name": "Laptop"}',
        "application/json",
    )

    assert isinstance(result, dict)
    assert result["id"] == 1
    assert result["name"] == "Laptop"


def test_parse_json_array() -> None:
    result = ResponseParser.parse(
        '[1, 2, 3]',
        "application/json",
    )

    assert isinstance(result, list)
    assert result == [1, 2, 3]


def test_parse_invalid_json() -> None:
    result = ResponseParser.parse(
        "{invalid json}",
        "application/json",
    )

    assert result is None


def test_parse_html() -> None:
    html = "<html><body>Hello</body></html>"

    result = ResponseParser.parse(
        html,
        "text/html",
    )

    assert result == html


def test_parse_plain_text() -> None:
    text = "Hello World"

    result = ResponseParser.parse(
        text,
        "text/plain",
    )

    assert result == text


def test_parse_binary() -> None:
    data = b"\x89PNG\r\n\x1a\n"

    result = ResponseParser.parse(
        data,
        "image/png",
    )

    assert result == data


def test_parse_utf8_bytes() -> None:
    result = ResponseParser.parse(
        b'{"success": true}',
        "application/json",
    )

    assert result == {
        "success": True,
    }


def test_parse_unknown_content_type_json() -> None:
    result = ResponseParser.parse(
        '{"value": 5}',
        "",
    )

    assert result == {
        "value": 5,
    }


def test_parse_unknown_content_type_text() -> None:
    text = "plain text"

    result = ResponseParser.parse(
        text,
        "",
    )

    assert result == text


def test_is_json() -> None:
    assert ResponseParser.is_json("application/json")
    assert ResponseParser.is_json("application/problem+json")
    assert not ResponseParser.is_json("text/html")


def test_is_html() -> None:
    assert ResponseParser.is_html("text/html")
    assert not ResponseParser.is_html("application/json")


def test_is_text() -> None:
    assert ResponseParser.is_text("text/plain")
    assert ResponseParser.is_text("application/json")
    assert ResponseParser.is_text("application/xml")
    assert not ResponseParser.is_text("image/png")


def test_is_binary() -> None:
    assert ResponseParser.is_binary("image/png")
    assert ResponseParser.is_binary("application/octet-stream")
    assert not ResponseParser.is_binary("application/json")
    assert not ResponseParser.is_binary("text/plain")
