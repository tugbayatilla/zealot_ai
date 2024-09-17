from ally_ai.chroma import Chroma, ChromaEmbeddingsVisualisor
import pytest

from ally_ai_core import Settings
from ally_ai_langchain import EmbeddingModel


@pytest.fixture
def instance():
    path='./tests/chroma/app-settings.yaml'

    chroma_settings = Settings(section='chromadb', path=path)
    embedding_settings = Settings(section='embeddings', path=path)
    
    embeddingModel = EmbeddingModel(settings=embedding_settings)
    chroma=Chroma(settings=chroma_settings, embeddingModel=embeddingModel)

    return ChromaEmbeddingsVisualisor(chroma=chroma, limit=10)

@pytest.mark.integration
def test_visualise(instance):
    figure = instance.visualise('what is an ally?', search_type='similarity')
    assert figure is not None