from __future__ import annotations

from jit.discovery.url_normalizer import URLNormalizer


def test_removes_query_parameters() -> None:
    url = "https://api.example.com/products?page=2"

    assert URLNormalizer.normalize(url) == "/products"


def test_removes_fragment() -> None:
    url = "https://api.example.com/products#section"

    assert URLNormalizer.normalize(url) == "/products"


def test_keeps_nested_paths() -> None:
    url = "https://api.example.com/api/v1/products/123"

    assert URLNormalizer.normalize(url) == "/api/v1/products/123"


def test_root_path() -> None:
    url = "https://api.example.com"

    assert URLNormalizer.normalize(url) == "/"


def test_relative_path() -> None:
    url = "/products"

    assert URLNormalizer.normalize(url) == "/products"
