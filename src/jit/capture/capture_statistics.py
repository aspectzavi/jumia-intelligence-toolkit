from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class CaptureStatistics:
    """
    Statistics collected during network capture.
    """

    requests: int = 0

    responses: int = 0

    failed_requests: int = 0

    redirected_requests: int = 0

    bytes_sent: int = 0

    bytes_received: int = 0

    def reset(self) -> None:
        """
        Reset all counters.
        """

        self.requests = 0
        self.responses = 0
        self.failed_requests = 0
        self.redirected_requests = 0
        self.bytes_sent = 0
        self.bytes_received = 0
