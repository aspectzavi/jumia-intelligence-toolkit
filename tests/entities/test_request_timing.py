from datetime import UTC, datetime, timedelta

from jit.entities.request_timing import RequestTiming


def test_start_now():
    timing = RequestTiming.start_now()

    assert timing.started_at is not None
    assert timing.ended_at is None


def test_finish():
    timing = RequestTiming.start_now()

    timing.finish()

    assert timing.is_completed
    assert timing.duration_ms is not None


def test_duration():
    timing = RequestTiming(
        started_at=datetime.now(UTC),
        ended_at=datetime.now(UTC) + timedelta(milliseconds=500),
    )

    assert timing.duration_ms >= 500


def test_to_dict():
    timing = RequestTiming.start_now()

    data = timing.to_dict()

    assert "started_at" in data


def test_from_dict():
    timing = RequestTiming.start_now()

    restored = RequestTiming.from_dict(timing.to_dict())

    assert restored.started_at == timing.started_at
