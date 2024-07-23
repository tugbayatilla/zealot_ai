from src.zealot_ai.settings.Settings import Settings


def test_default_path():
    settings = Settings()

    assert settings._path == './app-settings.yaml'


def test_change_default_path():
    new_path = 'no_such_file.yaml'
    settings = Settings(path=new_path)

    assert settings._path == new_path


def test_kwargs():
    new_path = 'no_such_file.yaml'
    settings = Settings(path=new_path, test=1)

    assert settings._path == new_path
    assert settings.kwargs == {'test': 1}
