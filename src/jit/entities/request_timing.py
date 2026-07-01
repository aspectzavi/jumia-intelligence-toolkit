from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any


@dataclass(slots=True)
class RequestTiming:
    """
    Represents the timing information for a network request.

    All timestamps are stored as UTC datetimes.
    """

    started_at: datetime
    ended_at: datetime | None = None

    @property
    def duration_ms(self) -> float | None:
        """
        Return the request duration in milliseconds.

        Returns:
            The duration in milliseconds if the request has
            completed, otherwise None.
        """

        if self.ended_at is None:
            return None

        return (self.ended_at - self.started_at).total_seconds() * 1000

    @property
    def is_completed(self) -> bool:
        """
        Whether the request has completed.
        """

        return self.ended_at is not None

    def finish(self) -> None:
        """
        Mark the request as completed.
        """

        self.ended_at = datetime.now(UTC)

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize the timing information.
        """

        return {
            "started_at": self.started_at.isoformat(),
            "ended_at": (self.ended_at.isoformat() if self.ended_at else None),
            "duration_ms": self.duration_ms,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> RequestTiming:
        """
        Deserialize timing information.
        """

        ended_at = data.get("ended_at")

        return cls(
            started_at=datetime.fromisoformat(data["started_at"]),
            ended_at=(datetime.fromisoformat(ended_at) if ended_at else None),
        )

    @classmethod
    def start_now(cls) -> RequestTiming:
        """
        Create a RequestTiming object with the current UTC time.
        """

        return cls(
            started_at=datetime.now(UTC),
        )

    def __str__(self) -> str:
        duration = self.duration_ms

        if duration is None:
            return "Running"

        return f"{duration:.2f} ms"
