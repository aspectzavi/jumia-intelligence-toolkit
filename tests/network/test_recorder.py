from jit.entities.http_request import HttpRequest
from jit.entities.http_response import HttpResponse
from jit.network.recorder import NetworkRecorder


def test_new_recorder_is_empty():
    recorder = NetworkRecorder()

    assert recorder.requests == []
    assert recorder.responses == []
    assert recorder.request_count == 0
    assert recorder.response_count == 0
    assert recorder.total_count == 0


def test_record_request():
    recorder = NetworkRecorder()

    request = HttpRequest(
        url="https://example.com",
    )

    recorder.record_request(request)

    assert recorder.request_count == 1
    assert recorder.requests[0] is request


def test_record_response():
    recorder = NetworkRecorder()

    response = HttpResponse(
        request_id="1",
        status=200,
    )

    recorder.record_response(response)

    assert recorder.response_count == 1
    assert recorder.responses[0] is response


def test_record_multiple_requests():
    recorder = NetworkRecorder()

    request1 = HttpRequest(
        url="https://example.com/1",
    )

    request2 = HttpRequest(
        url="https://example.com/2",
    )

    recorder.record_request(request1)
    recorder.record_request(request2)

    assert recorder.request_count == 2
    assert recorder.requests == [
        request1,
        request2,
    ]


def test_record_multiple_responses():
    recorder = NetworkRecorder()

    response1 = HttpResponse(
        request_id="1",
        status=200,
    )

    response2 = HttpResponse(
        request_id="2",
        status=404,
    )

    recorder.record_response(response1)
    recorder.record_response(response2)

    assert recorder.response_count == 2
    assert recorder.responses == [
        response1,
        response2,
    ]


def test_clear():
    recorder = NetworkRecorder()

    recorder.record_request(HttpRequest())

    recorder.record_response(
        HttpResponse(
            request_id="1",
            status=200,
        )
    )

    recorder.clear()

    assert recorder.requests == []
    assert recorder.responses == []
    assert recorder.total_count == 0


def test_total_count():
    recorder = NetworkRecorder()

    recorder.record_request(HttpRequest())

    recorder.record_request(HttpRequest())

    recorder.record_response(
        HttpResponse(
            request_id="1",
            status=200,
        )
    )

    assert recorder.total_count == 3


def test_request_order_is_preserved():
    recorder = NetworkRecorder()

    requests = [HttpRequest(url=f"https://example.com/{i}") for i in range(5)]

    for request in requests:
        recorder.record_request(request)

    assert recorder.requests == requests


def test_response_order_is_preserved():
    recorder = NetworkRecorder()

    responses = [
        HttpResponse(
            request_id=str(i),
            status=200,
        )
        for i in range(5)
    ]

    for response in responses:
        recorder.record_response(response)

    assert recorder.responses == responses


def test_clear_empty_recorder():
    recorder = NetworkRecorder()

    recorder.clear()

    assert recorder.request_count == 0
    assert recorder.response_count == 0
