from jit.openapi.openapi_operation import OpenApiOperation
from jit.openapi.openapi_schema import OpenApiSchema


def test_empty_operation():
    operation = OpenApiOperation()

    assert operation.to_dict() == {}


def test_request_body():
    operation = OpenApiOperation(
        request_body=OpenApiSchema(
            type="object",
        ),
    )

    assert operation.to_dict()["requestBody"] == {
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                }
            }
        }
    }


def test_response_body():
    operation = OpenApiOperation()

    operation.responses[200] = OpenApiSchema(
        type="object",
    )

    data = operation.to_dict()

    assert "responses" in data
    assert "200" in data["responses"]

    schema = (
        data["responses"]["200"]
        ["content"]["application/json"]
        ["schema"]
    )

    assert schema["type"] == "object"
