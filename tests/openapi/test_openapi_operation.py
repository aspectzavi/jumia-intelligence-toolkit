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
    operation = OpenApiOperation(
        response_body=OpenApiSchema(
            type="object",
        ),
    )

    assert operation.to_dict()["responses"] == {
        "200": {
            "description": "Successful response",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                    }
                }
            },
        }
    }
