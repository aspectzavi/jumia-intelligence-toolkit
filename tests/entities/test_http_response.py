from jit.entities.http_header import HttpHeader
from jit.entities.http_response import HttpResponse


def create_response() -> HttpResponse:
    response = HttpResponse(
        request_id="123",
        url="https://www.jumia.co.ke/api/products",
        status=200,
        status_text="OK",
    )

    response.add_header(
        HttpHeader(
            "Content-Type",
            "application/json",
        )
    )

    response.add_header(
        HttpHeader(
            "Server",
            "nginx",
        )
    )

    return response


def test_default_values():

    response = HttpResponse(
        request_id="1",
        status=200,
    )

    assert response.status == 200
    assert len(response.headers) == 0
    assert response.body is None


def test_add_header():
    response = HttpResponse(
        request_id="1",
        status=200,
    )

    response.add_header(
        HttpHeader(
            "Content-Type",
            "application/json",
        )
    )

    assert response.content_type == "application/json"


def test_header_map():

    response = create_response()

    assert response.header_map == {
        "content-type": "application/json",
        "server": "nginx",
    }


def test_content_type():

    response = create_response()

    assert response.content_type == "application/json"


def test_is_json():

    response = create_response()

    assert response.is_json


def test_not_json():

    response = HttpResponse(
        request_id="1",
        status=200,
    )

    response.add_header(
        HttpHeader(
            "Content-Type",
            "text/html",
        )
    )

    assert not response.is_json


def test_to_dict():

    response = create_response()

    data = response.to_dict()

    assert data["status"] == 200
    assert len(data["headers"]) == 2


def test_from_dict():

    response = create_response()

    restored = HttpResponse.from_dict(response.to_dict())

    assert restored.status == 200
    assert restored.status_text == "OK"
    assert len(restored.headers) == 2


def test_round_trip():

    response = create_response()

    restored = HttpResponse.from_dict(response.to_dict())

    assert restored.to_dict() == response.to_dict()
