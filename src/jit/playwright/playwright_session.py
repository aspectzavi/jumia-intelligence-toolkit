from __future__ import annotations


class PlaywrightSession:
    """
    Stores the current Playwright browser session.

    This class only manages state.
    It does not launch Playwright yet.
    """

    def __init__(self) -> None:
        self.browser = None
        self.context = None
        self.page = None

        self.started = False

    def _started(self) -> None:
        self.started = True

    def _stopped(self) -> None:
        self.started = False
