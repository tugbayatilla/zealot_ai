from ally_ai_core.settings.Settings import Settings
import pytest
import os
from tests import TEST_SETTINGS_PATH
import logging
from ..Utils import env_var_on_off


@pytest.fixture
def llm_settings():
    return Settings(section="llm")


def test_load_settings(llm_settings):
    assert llm_settings is not None


def test_api_key():
    with env_var_on_off("LLM__API_KEY", ""):
        settings = Settings(section="llm")
        assert settings["api_key"] == "<private-key>"


@pytest.mark.parametrize(
    "env_key, key, expected",
    [
        ("LLM__API_KEY", "api_key", "<new_api_key>"),
        ("LLM__api_KEY", "api_key", "<new_api_key>"),
        ("LLM__endpoint", "endpoint", "<new_endpoint>"),
    ],
)
def test_api_key_override(env_key, key, expected):
    with env_var_on_off(env_key, expected):
        settings = Settings(section="llm")
        assert settings[key] == expected


def test_default_path():
    assert Settings(section="llm").path == "./app-settings.yaml"


def test_change_default_path():
    new_path = "no_such_file.yaml"
    with pytest.raises(Exception):
        Settings(path=new_path)


def test_kwargs():
    settings = Settings(section="llm", test=1)

    assert settings["test"] == 1


def test_section_must_be_given():

    with pytest.raises(TypeError):
        Settings()


def test_no_app_setting_file_logs_error_once(caplog):

    with caplog.at_level(logging.DEBUG):
        with pytest.raises(Exception):
            Settings(section="", path="no_such_file")

    assert "Failed to read" in caplog.text


@pytest.mark.parametrize(
    "section,keys",
    [
        (
            "llm",
            [
                "api_key",
                "endpoint",
                "api_version",
                "model",
                "deployment_name",
                "temperature",
                "streaming",
            ],
        ),
        (
            "embeddings",
            ["api_key", "endpoint", "api_version", "model", "deployment_name"],
        ),
    ],
)
def test_app_setting_file(section, keys):
    settings = Settings(path=TEST_SETTINGS_PATH, section=section)

    assert settings is not None
    for key in keys:
        assert key in settings.keys()


def test_default_api_key():
    settings = Settings(path=TEST_SETTINGS_PATH, section="test-llm")

    assert settings["api_key"] == "<private-key>"


def test_override_default_api_key():
    new_api_key = "test_override_default_api_key"
    settings = Settings(
        path=TEST_SETTINGS_PATH, section="test-llm", api_key=new_api_key
    )
    print("settings:", settings)
    assert settings["api_key"] == new_api_key


def test_api_key_repr_having_more_than_7_chars():
    with env_var_on_off("LLM__API_KEY", "abcdef12345"):
        settings = Settings(path="./app-settings-small.yaml", section="llm")
        assert settings.__repr__() == "{'api_key': 'ab*****45'}"


def test_api_key_repr_having_less_than_7_chars():
    with env_var_on_off("LLM__API_KEY", "abcdef"):
        settings = Settings(path="./app-settings-small.yaml", section="llm")
        assert settings.__repr__() == "{'api_key': '*******'}"


def test_api_key_str_having_more_than_7_chars():
    with env_var_on_off("LLM__API_KEY", "abcdef12345"):
        settings = Settings(path="./app-settings-small.yaml", section="llm")
        assert settings.__str__() == "{'api_key': 'ab*****45'}"


def test_api_key_str_having_less_than_7_chars():
    with env_var_on_off("LLM__API_KEY", "abcdef"):
        settings = Settings(path="./app-settings-small.yaml", section="llm")
        assert settings.__str__() == "{'api_key': '*******'}"
