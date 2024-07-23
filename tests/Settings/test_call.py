from src.zealot_ai.settings.Settings import Settings
import pytest
from unittest.mock import patch
from tests import TEST_SETTINGS_PATH


def test_no_app_setting_file():
    settings = Settings(path='no_such_file')
    
    with patch('logging.error') as mock_error:
        with pytest.raises(Exception):
            settings(section='llm')

    mock_error.assert_called_once()


@pytest.mark.parametrize(
    'section,keys',
    [
        ('llm', ['api_key', 'endpoint', 'api_version', 'model',
         'deployment_name', 'temperature', 'streaming']),
        ('embeddings', ['api_key', 'endpoint',
         'api_version', 'model', 'deployment_name'])
    ]
)
def test_app_setting_file(section, keys):
    settings = Settings(path=TEST_SETTINGS_PATH)
    call = settings(section=section)

    assert call is not None
    for key in keys:
        assert key in call.keys()


def test_default_api_key():
    settings = Settings(path=TEST_SETTINGS_PATH)
    call = settings(section='llm')

    assert call['api_key'] == '<private-key>'


def test_override_default_api_key():
    new_api_key = 'new_api_key'
    settings = Settings(path=TEST_SETTINGS_PATH,
                        api_key=new_api_key)
    call = settings(section='llm')

    assert call['api_key'] == new_api_key
