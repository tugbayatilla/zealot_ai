from ally_ai_langchain import Embeddings


def test_settings_path_property():
    embeddings = Embeddings()

    assert embeddings.settings.path == './app-settings.yaml'


def test_settings_section_property():
    embeddings = Embeddings()

    assert embeddings.settings.section == 'embeddings'


def test_settings_has_api_key():
    embeddings = Embeddings()

    assert embeddings.settings['api_key'] == '<private-key>'
