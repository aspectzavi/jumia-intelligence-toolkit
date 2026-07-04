from __future__ import annotations

from urllib.parse import urlparse


class URLNormalizer:
    """
    Normalizes URLs into canonical API endpoint paths.

    Examples
    --------
    https://api.example.com/products?page=1
        -> /products

    https://api.example.com/products/123?sort=asc
        -> /products/123
    """

    @classmethod
    def normalize(
        cls,
        url: str,
    ) -> str:
        """
        Convert a full URL into a normalized endpoint path.

        Removes:

        - scheme
        - hostname
        - query string
        - fragment

        Ensures the returned path always starts with "/".
        """

        parsed = urlparse(url)

        path = parsed.path or "/"

        if not path.startswith("/"):
            path = f"/{path}"

        return path
