from jit.openapi.openapi_operation import OpenApiOperation
from jit.openapi.openapi_path import OpenApiPath


def test_empty_path():
    path = OpenApiPath()

    assert path.to_dict() == {}


def test_add_get_operation():
    path = OpenApiPath()

    path.add_operation(
        "GET",
        OpenApiOperation(),
    )

    assert "get" in path.to_dict()


def test_add_post_operation():
    path = OpenApiPath()

    path.add_operation(
        "POST",
        OpenApiOperation(),
    )

    assert "post" in path.to_dict()


def test_multiple_operations():
    path = OpenApiPath()

    path.add_operation(
        "GET",
        OpenApiOperation(),
    )

    path.add_operation(
        "POST",
        OpenApiOperation(),
    )

    assert len(path.to_dict()) == 2
