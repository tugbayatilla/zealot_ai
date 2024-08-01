import pytest
from ally_ai_langchain import EmbeddingModel
from openai import APIConnectionError


def test_default_embeddings_is_not_none():
    embeddings = EmbeddingModel()
    assert embeddings is not None


def test_embed_query_simple_raises_APIConnectionError():
    embeddings = EmbeddingModel()
    with pytest.raises(APIConnectionError):
        embeddings.embed_query('test')


def test_settings_path_property():
    embeddings = EmbeddingModel()

    assert embeddings.ally_settings.path == './app-settings.yaml'


def test_settings_section_property():
    embeddings = EmbeddingModel()

    assert embeddings.ally_settings.section == 'embeddings'


def test_settings_has_api_key():
    embeddings = EmbeddingModel()

    assert embeddings.ally_settings['api_key'] == '<private-key>'
