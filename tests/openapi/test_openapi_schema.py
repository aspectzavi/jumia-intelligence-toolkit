from jit.openapi.openapi_schema import OpenApiSchema


def test_empty_schema():
    schema = OpenApiSchema()

    assert schema.to_dict() == {}


def test_string_schema():
    schema = OpenApiSchema(
        type="string",
    )

    assert schema.to_dict() == {
        "type": "string",
    }


def test_object_schema():
    schema = OpenApiSchema(
        type="object",
    )

    schema.properties["id"] = OpenApiSchema(
        type="integer",
    )

    assert schema.to_dict() == {
        "type": "object",
        "properties": {
            "id": {
                "type": "integer",
            }
        },
    }
