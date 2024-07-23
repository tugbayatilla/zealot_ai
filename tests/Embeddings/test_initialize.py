from src.zealot_ai.models.langchain.openai.Embeddings import Embeddings


def test_default_embeddings_is_not_none():
    embeddings = Embeddings()

    assert embeddings is not None
