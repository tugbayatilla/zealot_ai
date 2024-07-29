import chromadb
from chromadb.config import Settings as ChromaSettings
from langchain_chroma import Chroma as LangChainChroma
from ally_ai_core import Settings
from ally_ai_langchain import Embeddings
from typing import Optional
import logging
from ChromaEmbeddingsVisualisation import ChromaEmbeddingsVisualisation

class AllyChroma(LangChainChroma):
    """
    Interited from LangChain Chroma
    """
    ally_settings: Settings = None

    def __init__(self,
                 settings: Optional[Settings] = None,
                 embeddings: Optional[Embeddings] = None,
                 **kwargs) -> None:

        if settings is None:
            settings = Settings(section='chromadb')
        if embeddings is None:
            embeddings = Embeddings()

        self.ally_settings = settings
        persist_directory = settings.pop('persist_directory')

        if persist_directory is not None and persist_directory:
            logging.info(f"Loading local chroma using '{persist_directory}' directory.")
            super().__init__(persist_directory=persist_directory,
                             embedding_function=embeddings,
                             create_collection_if_not_exists=False,
                             **kwargs)
        else:
            logging.info(f"Loading client chroma using '{settings['host']}' as host.")
            chroma_client = chromadb.HttpClient(
                **settings,
                settings=ChromaSettings(anonymized_telemetry=False))
            super().__init__(client=chroma_client,
                             embedding_function=embeddings,
                             create_collection_if_not_exists=False,
                             **kwargs)

    def visualise(self, query:str, limit: Optional[int] = None):
        cls = ChromaEmbeddingsVisualisation(self, limit=limit)
        cls(query=query)