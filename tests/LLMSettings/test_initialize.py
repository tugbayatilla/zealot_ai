import pytest
from src.zealot_ai.settings.LLMSettings import LLMSettings
from tests import TEST_SETTINGS_PATH


def test_no_app_setting_file_raises_exception():

    with pytest.raises(Exception):
        _ = LLMSettings(path='')


def test_init():
    settings = LLMSettings(path=TEST_SETTINGS_PATH)
    assert settings.api_key == '<private-key>'
