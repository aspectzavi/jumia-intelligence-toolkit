from __future__ import annotations

import json

from jit.analyzer.endpoint_analyzer import EndpointAnalyzer
from jit.entities.api_endpoint import ApiEndpoint
from jit.entities.header_collection import HeaderCollection
from jit.entities.http_header import HttpHeader
from jit.entities.http_response import HttpResponse


def make_response(
    *,
    status: int = 200,
    content_type: str | None = "application/json",
    body: bytes | str | None = b"{}",
) -> HttpResponse:
    headers = HeaderCollection()

    if content_type is not None:
        headers.add(HttpHeader("Content-Type", content_type))

    return HttpResponse(
        request_id="1",
        status=status,
        body=body,
        headers=headers,
    )


def make_endpoint() -> ApiEndpoint:
    return ApiEndpoint(path="/api/products", method="GET")


def test_analyze_json_response_infers_schema():
    endpoint = make_endpoint()
    endpoint.add_response(
        make_response(
            body=json.dumps(
                {"id": 1, "name": "Phone"},
            ).encode("utf-8"),
        )
    )

    EndpointAnalyzer().analyze(endpoint)

    assert endpoint.response_schema is not None
    assert endpoint.status_codes == {200: 1}
    assert endpoint.content_types == {"application/json": 1}
    assert endpoint.examples == [{"id": 1, "name": "Phone"}]
    assert endpoint.confidence == 0.35


def test_analyze_merges_schema_across_multiple_responses():
    endpoint = make_endpoint()
    endpoint.add_response(
        make_response(body=json.dumps({"id": 1}).encode("utf-8")),
    )
    endpoint.add_response(
        make_response(
            body=json.dumps({"id": 2, "discount": None}).encode("utf-8"),
        ),
    )

    EndpointAnalyzer().analyze(endpoint)

    assert endpoint.response_count == 2
    assert endpoint.response_schema is not None
    field_names = {field.name for field in endpoint.response_schema}
    assert field_names == {"id", "discount"}


def test_analyze_non_json_response_does_not_crash():
    endpoint = make_endpoint()
    endpoint.add_response(
        make_response(
            content_type="text/html",
            body=b"<html></html>",
        ),
    )

    EndpointAnalyzer().analyze(endpoint)

    assert endpoint.response_schema is None
    assert endpoint.examples == ["<html></html>"]
    assert endpoint.status_codes == {200: 1}


def test_analyze_empty_body_is_safe():
    endpoint = make_endpoint()
    endpoint.add_response(make_response(body=None))

    EndpointAnalyzer().analyze(endpoint)

    assert endpoint.response_schema is None
    assert endpoint.examples == []
    assert endpoint.confidence == 0.0
