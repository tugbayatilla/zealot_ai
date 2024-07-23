from src.ally_ai.settings.Settings import Settings
import pytest

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
