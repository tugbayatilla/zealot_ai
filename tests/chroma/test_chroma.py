from ally_ai.chroma import Chroma
import pytest

from ally_ai_core import Settings
from ally_ai_langchain import EmbeddingModel


@pytest.fixture
def instance():
    path = "./tests/chroma/app-settings.yaml"

    chroma_settings = Settings(section="chromadb", path=path)
    embedding_settings = Settings(section="embeddings", path=path)

    embeddingModel = EmbeddingModel(settings=embedding_settings)
    return Chroma(settings=chroma_settings, embeddingModel=embeddingModel)


@pytest.mark.integration
def test_query_document(instance):
    results = instance.query("what is an ally?", n_results=2, include=["documents"])
    retrieved_documents = results["documents"][0]

    assert len(retrieved_documents) == 2


@pytest.mark.integration
def test_query_embeddings(instance):
    results = instance.query("what is an ally?", n_results=2, include=["embeddings"])
    retrieved_documents = results["embeddings"][0]

    assert len(retrieved_documents) == 2


@pytest.mark.integration
def test_multiple_query(instance):
    queries = ["what is an ally?", "do we need it?"]
    results = instance.query(query_texts=queries, n_results=2, include=["documents"])
    retrieved_documents = results["documents"][0]

    assert len(retrieved_documents) == 2


@pytest.mark.integration
def test_availability():
    path = "./tests/chroma/app-settings.yaml"

    chroma_settings = Settings(section="chromadb_unavailable", path=path)
    embedding_settings = Settings(section="embeddings", path=path)

    embeddingModel = EmbeddingModel(settings=embedding_settings)
    with pytest.raises(Exception) as e_info:
        _ = Chroma(settings=chroma_settings, embeddingModel=embeddingModel)
    print(e_info)
