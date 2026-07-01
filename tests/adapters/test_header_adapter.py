from jit.adapters.header_adapter import HeaderAdapter
from jit.entities.header_collection import HeaderCollection
from jit.entities.http_header import HttpHeader


def test_empty():
    headers = HeaderAdapter.empty()

    assert isinstance(headers, HeaderCollection)
    assert len(headers) == 0


def test_from_mapping():
    collection = HeaderAdapter.from_mapping(
        {
            "Content-Type": "application/json",
            "Accept": "*/*",
        }
    )

    assert isinstance(collection, HeaderCollection)
    assert len(collection) == 2

    assert collection.get("content-type") == "application/json"
    assert collection.get("accept") == "*/*"


def test_from_mapping_none():
    collection = HeaderAdapter.from_mapping(None)

    assert isinstance(collection, HeaderCollection)
    assert len(collection) == 0


def test_from_pairs():
    collection = HeaderAdapter.from_pairs(
        [
            (
                "Content-Type",
                "application/json",
            ),
            (
                "Accept",
                "*/*",
            ),
        ]
    )

    assert len(collection) == 2
    assert collection.get("content-type") == "application/json"
    assert collection.get("accept") == "*/*"


def test_from_pairs_none():
    collection = HeaderAdapter.from_pairs(None)

    assert len(collection) == 0


def test_to_mapping():
    collection = HeaderCollection()

    collection.add(
        HttpHeader(
            "Content-Type",
            "application/json",
        )
    )

    collection.add(
        HttpHeader(
            "Accept",
            "*/*",
        )
    )

    mapping = HeaderAdapter.to_mapping(collection)

    assert mapping == {
        "content-type": "application/json",
        "accept": "*/*",
    }


def test_to_pairs():
    collection = HeaderCollection()

    collection.add(
        HttpHeader(
            "Content-Type",
            "application/json",
        )
    )

    collection.add(
        HttpHeader(
            "Accept",
            "*/*",
        )
    )

    pairs = HeaderAdapter.to_pairs(collection)

    assert pairs == [
        (
            "content-type",
            "application/json",
        ),
        (
            "accept",
            "*/*",
        ),
    ]


def test_clone():
    original = HeaderCollection()

    original.add(
        HttpHeader(
            "Content-Type",
            "application/json",
        )
    )

    clone = HeaderAdapter.clone(original)

    assert clone is not original
    assert len(clone) == len(original)

    assert clone.get("content-type") == original.get("content-type")


def test_serialize():
    collection = HeaderCollection()

    collection.add(
        HttpHeader(
            "Accept",
            "*/*",
        )
    )

    data = HeaderAdapter.serialize(collection)

    assert data == [
        {
            "name": "accept",
            "value": "*/*",
        }
    ]


def test_deserialize():
    data = [
        {
            "name": "content-type",
            "value": "application/json",
        },
        {
            "name": "accept",
            "value": "*/*",
        },
    ]

    collection = HeaderAdapter.deserialize(data)

    assert isinstance(collection, HeaderCollection)
    assert len(collection) == 2

    assert collection.get("content-type") == "application/json"

    assert collection.get("accept") == "*/*"
