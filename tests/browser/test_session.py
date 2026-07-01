from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

from jit.browser.session import SessionManager


def test_state_path_comes_from_settings(tmp_path):
    with patch(
        "jit.browser.session.settings.state_path",
        str(tmp_path / "state.json"),
    ):
        manager = SessionManager()

        assert manager.state_path == tmp_path / "state.json"


def test_exists_returns_false(tmp_path):
    with patch(
        "jit.browser.session.settings.state_path",
        str(tmp_path / "missing.json"),
    ):
        manager = SessionManager()

        assert manager.exists is False


def test_exists_returns_true(tmp_path):
    path = tmp_path / "state.json"
    path.write_text("{}")

    with patch(
        "jit.browser.session.settings.state_path",
        str(path),
    ):
        manager = SessionManager()

        assert manager.exists is True


def test_is_valid_returns_false_when_missing(tmp_path):
    with patch(
        "jit.browser.session.settings.state_path",
        str(tmp_path / "missing.json"),
    ):
        manager = SessionManager()

        assert manager.is_valid is False


def test_is_valid_returns_false_when_empty(tmp_path):
    path = tmp_path / "state.json"
    path.touch()

    with patch(
        "jit.browser.session.settings.state_path",
        str(path),
    ):
        manager = SessionManager()

        assert manager.is_valid is False


def test_is_valid_returns_false_for_invalid_json(tmp_path):
    path = tmp_path / "state.json"

    path.write_text(
        "{invalid json",
        encoding="utf-8",
    )

    with patch(
        "jit.browser.session.settings.state_path",
        str(path),
    ):
        manager = SessionManager()

        assert manager.is_valid is False


def test_is_valid_returns_true(tmp_path):
    path = tmp_path / "state.json"

    path.write_text(
        json.dumps({"cookies": []}),
        encoding="utf-8",
    )

    with patch(
        "jit.browser.session.settings.state_path",
        str(path),
    ):
        manager = SessionManager()

        assert manager.is_valid is True


def test_is_valid_handles_unexpected_exception(tmp_path):
    path = tmp_path / "state.json"

    path.write_text(
        "{}",
        encoding="utf-8",
    )

    with patch(
        "jit.browser.session.settings.state_path",
        str(path),
    ):
        manager = SessionManager()

        with patch.object(
            Path,
            "open",
            side_effect=OSError("boom"),
        ):
            assert manager.is_valid is False


@pytest.mark.asyncio
async def test_save_creates_parent_directory(tmp_path):
    path = tmp_path / "nested" / "state.json"

    with patch(
        "jit.browser.session.settings.state_path",
        str(path),
    ):
        manager = SessionManager()

        context = AsyncMock()

        await manager.save(context)

        assert path.parent.exists()


@pytest.mark.asyncio
async def test_save_calls_storage_state(tmp_path):
    path = tmp_path / "state.json"

    with patch(
        "jit.browser.session.settings.state_path",
        str(path),
    ):
        manager = SessionManager()

        context = AsyncMock()

        await manager.save(context)

        context.storage_state.assert_awaited_once_with(path=str(path))


@pytest.mark.asyncio
async def test_save_overwrites_existing_file(tmp_path):
    path = tmp_path / "state.json"

    path.write_text(
        "old",
        encoding="utf-8",
    )

    with patch(
        "jit.browser.session.settings.state_path",
        str(path),
    ):
        manager = SessionManager()

        context = AsyncMock()

        await manager.save(context)

        context.storage_state.assert_awaited_once()


@pytest.mark.asyncio
async def test_save_propagates_storage_state_error(tmp_path):
    path = tmp_path / "state.json"

    with patch(
        "jit.browser.session.settings.state_path",
        str(path),
    ):
        manager = SessionManager()

        context = AsyncMock()

        context.storage_state.side_effect = RuntimeError("failed")

        with pytest.raises(RuntimeError):
            await manager.save(context)
