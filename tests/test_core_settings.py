from ally_ai_core import Settings
import pytest
from unittest.mock import patch
from tests import TEST_SETTINGS_PATH


def test_default_path():
    settings = Settings(section='llm')

    assert settings.path == './app-settings.yaml'


def test_change_default_path():
    new_path = 'no_such_file.yaml'
    with pytest.raises(Exception):
        Settings(path=new_path)



def test_kwargs():
    settings = Settings(section='llm', test=1)

    assert settings['test'] == 1

def test_section_must_be_given():
    
    with pytest.raises(TypeError) as ex:
        Settings()


def test_no_app_setting_file_logs_error_once():
    
    with patch('logging.error') as mock_error:
        with pytest.raises(Exception) as ex:
            Settings(section='',path='no_such_file')

    print(ex)
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
    settings = Settings(path=TEST_SETTINGS_PATH, section=section)

    assert settings is not None
    for key in keys:
        assert key in settings.keys()


def test_default_api_key():
    settings = Settings(path=TEST_SETTINGS_PATH, section='llm')

    assert settings['api_key'] == '<private-key>'


def test_override_default_api_key():
    new_api_key = 'new_api_key'
    settings = Settings(path=TEST_SETTINGS_PATH,
                        section='llm',
                        api_key=new_api_key)
    print('settings:', settings)
    assert settings['api_key'] == new_api_key
