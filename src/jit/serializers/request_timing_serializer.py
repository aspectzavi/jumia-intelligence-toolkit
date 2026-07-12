from __future__ import annotations

from datetime import datetime
from typing import Any

from jit.entities.request_timing import RequestTiming


class RequestTimingSerializer:
    """
    Serializes RequestTiming objects.
    """

    @staticmethod
    def to_dict(
        timing: RequestTiming,
    ) -> dict[str, Any]:
        """
        Serialize timing information.
        """

        return {
            "started_at": timing.started_at.isoformat(),
            "ended_at": (
                timing.ended_at.isoformat()
                if timing.ended_at is not None
                else None
            ),
            "duration_ms": timing.duration_ms,
        }

    @staticmethod
    def from_dict(
        data: dict[str, Any],
    ) -> RequestTiming:
        """
        Deserialize timing information.
        """

        ended_at = data.get("ended_at")

        return RequestTiming(
            started_at=datetime.fromisoformat(
                data["started_at"]
            ),
            ended_at=(
                datetime.fromisoformat(ended_at)
                if ended_at is not None
                else None
            ),
        )
