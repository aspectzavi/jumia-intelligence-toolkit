from datetime import UTC, datetime, timedelta

from jit.entities.request_timing import RequestTiming


def test_start_now():

    timing = RequestTiming.start_now()

    assert timing.started_at is not None
    assert timing.ended_at is None
    assert not timing.is_completed


def test_finish():

    timing = RequestTiming.start_now()

    timing.finish()

    assert timing.is_completed
    assert timing.ended_at is not None
    assert timing.duration_ms is not None
    assert timing.duration_ms >= 0


def test_duration():

    timing = RequestTiming(
        started_at=datetime.now(UTC),
        ended_at=datetime.now(UTC)
        + timedelta(milliseconds=500),
    )

    assert timing.duration_ms >= 500


def test_to_dict():

    timing = RequestTiming.start_now()

    data = timing.to_dict()

    assert "started_at" in data
    assert "ended_at" in data


def test_from_dict():

    timing = RequestTiming.start_now()

    timing.finish()

    restored = RequestTiming.from_dict(
        timing.to_dict()
    )

    assert restored.started_at == timing.started_at
    assert restored.ended_at == timing.ended_at
    assert restored.is_completed == timing.is_completed


def test_round_trip():

    original = RequestTiming.start_now()

    original.finish()

    restored = RequestTiming.from_dict(
        original.to_dict()
    )

    assert restored.to_dict() == original.to_dict()