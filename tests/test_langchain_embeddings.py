import pytest
from ally_ai_langchain import Embeddings
from openai import APIConnectionError


def test_default_embeddings_is_not_none():
    embeddings = Embeddings()
    assert embeddings is not None


def test_embed_query_simple_raises_APIConnectionError():
    embeddings = Embeddings()
    with pytest.raises(APIConnectionError):
        embeddings.embed_query('test')


def test_settings_path_property():
    embeddings = Embeddings()

    assert embeddings.settings.path == './app-settings.yaml'


def test_settings_section_property():
    embeddings = Embeddings()

    assert embeddings.settings.section == 'embeddings'


def test_settings_has_api_key():
    embeddings = Embeddings()

    assert embeddings.settings['api_key'] == '<private-key>'
