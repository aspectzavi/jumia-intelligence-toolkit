from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime


@dataclass(slots=True)
class NetworkEvent:
    """
    Represents a raw browser network event.
    """

    timestamp: datetime

    event: str

    request_id: str

    @classmethod
    def create(
        cls,
        event: str,
        request_id: str,
    ) -> NetworkEvent:
        return cls(
            timestamp=datetime.now(UTC),
            event=event,
            request_id=request_id,
        )
