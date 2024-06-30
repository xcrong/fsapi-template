from .config import app_config


def test_app_config_when_read_default_envs():
    assert app_config.api_key == "ak-12345"
