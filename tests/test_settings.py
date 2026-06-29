from jit.configs.settings import settings


def test_base_url():
    assert settings.base_url.startswith("https")


VALID_BROWSERS = {"chromium", "firefox", "webkit"}


def test_browser():
    assert settings.browser in VALID_BROWSERS


def test_timeout():
    assert settings.timeout > 0
