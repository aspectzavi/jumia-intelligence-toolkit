from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass(slots=True)
class NetworkEvent:
    """
    Represents a browser network event.
    """

    event: str

    request_id: str

    timestamp: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    payload: dict[str, Any] = field(
        default_factory=dict
    )

    @classmethod
    def create(
        cls,
        *,
        event: str,
        request_id: str,
        payload: dict[str, Any] | None = None,
    ) -> NetworkEvent:
        """
        Create a new network event with the current timestamp.
        """

        return cls(
            event=event,
            request_id=request_id,
            payload=payload or {},
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "event": self.event,
            "request_id": self.request_id,
            "timestamp": self.timestamp.isoformat(),
            "payload": self.payload,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> NetworkEvent:
        return cls(
            event=data["event"],
            request_id=data["request_id"],
            timestamp=datetime.fromisoformat(
                data["timestamp"]
            ),
            payload=data.get("payload", {}),
        )

    def __str__(self) -> str:
        return f"{self.event} ({self.request_id})"
