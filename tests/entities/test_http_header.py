from jit.entities.http_header import HttpHeader


def test_create_header():
    header = HttpHeader(
        name="Content-Type",
        value="application/json",
    )

    assert header.name == "content-type"
    assert header.value == "application/json"


def test_to_dict():
    header = HttpHeader(
        name="Accept",
        value="application/json",
    )

    assert header.to_dict() == {
        "name": "accept",
        "value": "application/json",
    }


def test_from_dict():
    data = {
        "name": "Host",
        "value": "jumia.co.ke",
    }

    header = HttpHeader.from_dict(data)

    assert header.name == "host"
    assert header.value == "jumia.co.ke"


def test_string_representation():
    header = HttpHeader(
        name="User-Agent",
        value="Playwright",
    )

    assert str(header) == "user-agent: Playwright"
