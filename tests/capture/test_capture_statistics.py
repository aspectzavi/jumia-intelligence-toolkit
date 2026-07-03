from __future__ import annotations

from jit.capture.capture_statistics import CaptureStatistics


def test_initial_statistics():
    stats = CaptureStatistics()

    assert stats.requests == 0
    assert stats.responses == 0
    assert stats.failed_requests == 0


def test_increment_requests():
    stats = CaptureStatistics()

    stats.requests += 1
    stats.requests += 1

    assert stats.requests == 2


def test_increment_responses():
    stats = CaptureStatistics()

    stats.responses += 1

    assert stats.responses == 1
