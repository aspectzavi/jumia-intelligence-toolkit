from __future__ import annotations

from jit.discovery.api_mapper import ApiMapper
from jit.playwright.event_handlers import EventHandlers
from jit.playwright.request_mapper import RequestLike
from jit.playwright.response_mapper import ResponseLike


class FakeRequest(RequestLike):
    def __init__(self) -> None:
        self.url = "https://api.example.com/products"
        self.method = "GET"
        self.resource_type = "xhr"
        self.headers: dict[str, str] = {}
        self.post_data: str | None = None


class FakeResponse(ResponseLike):
    def __init__(self) -> None:
        self.status = 200
        self.status_text = "OK"
        self.url = "https://api.example.com/products"
        self.headers: dict[str, str] = {}


def test_request_event_creates_endpoint() -> None:
    mapper = ApiMapper()
    handlers = EventHandlers(mapper)

    request: RequestLike = FakeRequest()

    handlers.on_request(request)

    endpoint = mapper.get(
        "GET",
        "/products",
    )

    assert endpoint is not None
    assert len(endpoint.requests) == 1


def test_response_event_attaches_response() -> None:
    mapper = ApiMapper()
    handlers = EventHandlers(mapper)

    request: RequestLike = FakeRequest()

    handlers.on_request(request)

    response: ResponseLike = FakeResponse()

    assert handlers.last_request is not None

    handlers.on_response(
        request_id=handlers.last_request.id,
        response=response,
    )

    endpoint = mapper.get(
        "GET",
        "/products",
    )

    assert endpoint is not None
    assert len(endpoint.responses) == 1
