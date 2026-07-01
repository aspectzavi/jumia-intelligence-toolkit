from jit.entities.header_collection import HeaderCollection
from jit.entities.http_header import HttpHeader


def test_empty_collection():

    headers = HeaderCollection()

    assert len(headers) == 0


def test_add_header():

    headers = HeaderCollection()

    headers.add(
        HttpHeader(
            "Content-Type",
            "application/json",
        )
    )

    assert len(headers) == 1


def test_get_header_case_insensitive():

    headers = HeaderCollection()

    headers.add(
        HttpHeader(
            "Content-Type",
            "application/json",
        )
    )

    assert headers.get("content-type") == "application/json"

    assert headers.get("CONTENT-TYPE") == "application/json"


def test_has_header():

    headers = HeaderCollection()

    headers.add(
        HttpHeader(
            "Authorization",
            "Bearer token",
        )
    )

    assert headers.has("authorization")

    assert not headers.has("cookie")


def test_content_type_property():

    headers = HeaderCollection()

    headers.add(
        HttpHeader(
            "Content-Type",
            "application/json",
        )
    )

    assert headers.content_type == "application/json"


def test_content_length_property():

    headers = HeaderCollection()

    headers.add(
        HttpHeader(
            "Content-Length",
            "128",
        )
    )

    assert headers.content_length == 128


def test_content_length_invalid():

    headers = HeaderCollection()

    headers.add(
        HttpHeader(
            "Content-Length",
            "abc",
        )
    )

    assert headers.content_length is None


def test_get_all():

    headers = HeaderCollection()

    headers.add(
        HttpHeader(
            "Set-Cookie",
            "A=1",
        )
    )

    headers.add(
        HttpHeader(
            "Set-Cookie",
            "B=2",
        )
    )

    assert headers.get_all("set-cookie") == [
        "A=1",
        "B=2",
    ]


def test_to_dict_roundtrip():

    headers = HeaderCollection()

    headers.add(
        HttpHeader(
            "Accept",
            "*/*",
        )
    )

    data = headers.to_dict()

    restored = HeaderCollection.from_dict(data)

    assert restored.get("accept") == "*/*"


def test_contains():

    headers = HeaderCollection()

    headers.add(
        HttpHeader(
            "Host",
            "jumia.co.ke",
        )
    )

    assert "host" in headers

    assert "authorization" not in headers


def test_getitem():

    headers = HeaderCollection()

    headers.add(
        HttpHeader(
            "Host",
            "jumia.co.ke",
        )
    )

    assert headers["HOST"] == "jumia.co.ke"


def test_repr():

    headers = HeaderCollection()

    assert "HeaderCollection" in repr(headers)
