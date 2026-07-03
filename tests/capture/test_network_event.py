from __future__ import annotations

from datetime import datetime

from jit.capture.network_event import NetworkEvent


def test_create_event():
    event = NetworkEvent.create(
        event="REQUEST_STARTED",
        request_id="abc123",
    )

    assert event.event == "REQUEST_STARTED"
    assert event.request_id == "abc123"
    assert isinstance(event.timestamp, datetime)


def test_manual_event():
    now = datetime.now()

    event = NetworkEvent(
        timestamp=now,
        event="RESPONSE_RECEIVED",
        request_id="xyz",
    )

    assert event.timestamp == now
    assert event.event == "RESPONSE_RECEIVED"
    assert event.request_id == "xyz"
