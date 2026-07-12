from __future__ import annotations

from datetime import UTC, datetime

from jit.entities.request_timing import RequestTiming
from jit.serializers.request_timing_serializer import (
    RequestTimingSerializer,
)


def test_to_dict() -> None:
    started = datetime(
        2026,
        1,
        1,
        tzinfo=UTC,
    )

    ended = datetime(
        2026,
        1,
        1,
        0,
        0,
        1,
        tzinfo=UTC,
    )

    timing = RequestTiming(
        started_at=started,
        ended_at=ended,
    )

    result = RequestTimingSerializer.to_dict(
        timing
    )

    assert result["started_at"] == started.isoformat()
    assert result["ended_at"] == ended.isoformat()
    assert result["duration_ms"] == 1000.0


def test_from_dict() -> None:
    data = {
        "started_at": "2026-01-01T00:00:00+00:00",
        "ended_at": "2026-01-01T00:00:01+00:00",
        "duration_ms": 1000.0,
    }

    timing = RequestTimingSerializer.from_dict(
        data
    )

    assert timing.started_at.isoformat() == data["started_at"]
    assert timing.ended_at is not None
    assert timing.ended_at.isoformat() == data["ended_at"]


def test_round_trip() -> None:
    original = RequestTiming.start_now()

    original.finish()

    restored = RequestTimingSerializer.from_dict(
        RequestTimingSerializer.to_dict(
            original
        )
    )

    assert (
        restored.started_at
        == original.started_at
    )

    assert (
        restored.ended_at
        == original.ended_at
    )
