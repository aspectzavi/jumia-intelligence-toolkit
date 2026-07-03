from __future__ import annotations

from jit.discovery.api_mapper import ApiMapper
from jit.playwright.event_handlers import EventHandlers


class FakeRequest:
    def __init__(self) -> None:
        self._url = "https://api.example.com/products"

    @property
    def url(self) -> str:
        return self._url

    @property
    def method(self) -> str:
        return "GET"

    @property
    def resource_type(self) -> str:
        return "xhr"

    @property
    def headers(self) -> dict[str, str]:
        return {}

    @property
    def post_data(self) -> str | None:
        return None


class FakeResponse:
    def __init__(self, request: FakeRequest) -> None:
        self._status = 200
        self._status_text = "OK"
        self._url = "https://api.example.com/products"
        self._headers: dict[str, str] = {}

        self._request = request

    @property
    def status(self) -> int:
        return self._status

    @property
    def status_text(self) -> str:
        return self._status_text

    @property
    def url(self) -> str:
        return self._url

    @property
    def headers(self) -> dict[str, str]:
        return self._headers

    @property
    def request(self) -> FakeRequest:
        return self._request


def test_request_event_creates_endpoint() -> None:
    mapper = ApiMapper()
    handlers = EventHandlers(mapper)

    request = FakeRequest()
    handlers.on_request(request)

    endpoint = mapper.get("GET", "/products")

    assert endpoint is not None
    assert len(endpoint.requests) == 1


def test_response_event_attaches_response() -> None:
    mapper = ApiMapper()
    handlers = EventHandlers(mapper)

    request = FakeRequest()
    handlers.on_request(request)

    response = FakeResponse(request)

    # FIX: no request_id anymore
    handlers.on_response(response=response)

    endpoint = mapper.get("GET", "/products")

    assert endpoint is not None
    assert len(endpoint.responses) == 1
