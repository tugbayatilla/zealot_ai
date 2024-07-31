import chromadb
from chromadb.config import Settings as ChromaSettings
from langchain_chroma import Chroma as LangChainChroma
from ally_ai_core import Settings
from ally_ai_langchain import EmbeddingModel
from typing import Optional
import logging

class Chroma(LangChainChroma):
    """
    Interited from LangChain Chroma
    """
    ally_settings: Settings = None

    def __init__(self,
                 settings: Optional[Settings] = None,
                 embeddingModel: Optional[EmbeddingModel] = None,
                 **kwargs) -> None:

        if settings is None:
            settings = Settings(section='chromadb')
        if embeddingModel is None:
            embeddingModel = EmbeddingModel()

        self.ally_settings = settings
        persist_directory = settings.pop('persist_directory') if 'persist_directory' in settings else None

        chroma_settings = ChromaSettings(anonymized_telemetry=False)
        if persist_directory is not None and persist_directory:
            logging.info(f"Loading chroma using '{persist_directory}' directory.")
            super().__init__(persist_directory=persist_directory,
                             embedding_function=embeddingModel,
                             create_collection_if_not_exists=False,
                             client_settings=chroma_client
                             **kwargs)
        else:
            logging.info(f"Loading chroma client using '{settings['host']}' as host.")
            chroma_client = chromadb.HttpClient(
                **settings,
                settings=chroma_settings)
            super().__init__(client=chroma_client,
                             embedding_function=embeddingModel,
                             create_collection_if_not_exists=False,
                             **kwargs)
