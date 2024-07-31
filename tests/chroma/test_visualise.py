from ally_ai.chroma import Chroma, ChromaEmbeddingsVisualisation
import pytest

from ally_ai_core.settings.Settings import Settings
from ally_ai_langchain import EmbeddingModel


@pytest.fixture
def instance():
    chroma_settings = Settings(section='chromadb', path='./app-settings-integration.yaml')
    embedding_settings = Settings(section='embeddings', path='./app-settings-integration.yaml')
    embeddingModel = EmbeddingModel(settings=embedding_settings)
    chroma=Chroma(settings=chroma_settings, embeddingModel=embeddingModel)

    return ChromaEmbeddingsVisualisation(chroma=chroma, limit=10)

@pytest.mark.integration
def test_visualise(instance):
    figure = instance.visualise('what is an ally?', search_type='similarity')
    assert figure is not None