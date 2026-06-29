from jit.configs.settings import settings


def test_base_url():
    assert settings.base_url.startswith("https")


def test_browser():
    assert settings.browser == "chromium"


def test_timeout():
    assert settings.timeout > 0
