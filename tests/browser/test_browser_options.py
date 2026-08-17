from __future__ import annotations

from jit.browser.browser_options import BrowserOptions


def test_default_options():
    options = BrowserOptions()

    assert options.headless is True
    assert options.timeout == 30000
    assert options.viewport_width == 1280
    assert options.viewport_height == 720
    assert options.record_requests is True
    assert options.record_responses is True
    assert options.record_images is False
    assert options.record_scripts is True


def test_custom_options():
    options = BrowserOptions(
        headless=False,
        timeout=10000,
        viewport_width=1920,
        viewport_height=1080,
    )

    assert options.headless is False
    assert options.timeout == 10000
    assert options.viewport_width == 1920
    assert options.viewport_height == 1080