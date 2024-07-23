from langchain_openai import AzureChatOpenAI
from langchain_openai import AzureOpenAIEmbeddings
from typing import Literal, Union
from pydantic import BaseModel
from ..core import Settings
import logging

from langchain_chroma import Chroma
from langchain_core.vectorstores import VectorStoreRetriever
import chromadb
from chromadb.config import Settings


class ModelManager:

    def __init__(self, configManager: Settings) -> None:
        self._config = configManager

    def get_llm(self, schema: Union[dict, BaseModel, None] = None, streaming=False):
        """ 
        Returns llm model
        """

        llm_config = self._config.get_section(name='llm')

        llm = AzureChatOpenAI(
            api_key=llm_config['key'],
            azure_endpoint=llm_config['endpoint'],
            api_version=llm_config['api_version'],
            model=llm_config['model'],
            deployment_name=llm_config['deployment_name'],
            temperature=llm_config['temperature'],
            streaming=streaming
        )
        if schema:
            llm = llm.with_structured_output(schema=schema)

        return llm

    def get_embeding_model(self):
        """ 
        Returns embeding model
        """

        embeddings_config = self._config.get_section(name='embeddings')

        # You need to deploy your own embedding model as well as your own chat completion model
        embed_model = AzureOpenAIEmbeddings(
            api_key=embeddings_config['key'],
            azure_endpoint=embeddings_config['endpoint'],
            api_version=embeddings_config['api_version'],
            model=embeddings_config['model'],
            azure_deployment=embeddings_config['deployment_name'],
        )

        return embed_model

    def get_retriever(self, type='mmr', k=6) -> VectorStoreRetriever:
        """
            returns VectorStoreRetriever using chromadb 
        """
        config = self._config.get_section(name='vectordb')

        endpoint = config['endpoint']
        port = config['port']

        settings = Settings(anonymized_telemetry=False)

        chroma_client = chromadb.HttpClient(
            host=endpoint,
            port=port,
            settings=settings)

        embeddings = self.get_embeding_model()

        db = Chroma(
            client=chroma_client,
            embedding_function=embeddings,
            create_collection_if_not_exists=False)

        retriever = db.as_retriever(search_type=type, search_kwargs={"k": k})

        return retriever

    def get_local_retriever(self,
                            persist_directory="../chroma_db",
                            search_type: Literal['mmr',
                                                 'similarity_score_threshold', 'similarity'] = 'mmr',
                            **search_kwargs) -> VectorStoreRetriever:
        """
            returns VectorStoreRetriever using chromadb 
        """

        embedding_function = self.get_embeding_model()

        # settings = Settings(anonymized_telemetry=False)
        db = Chroma(persist_directory=persist_directory,
                    embedding_function=embedding_function,
                    create_collection_if_not_exists=False)

        # if search_type == 'mmr' and search_kwargs:
        #     search_kwargs = {"k": 6}
        # if search_type == "similarity_score_threshold" and search_kwargs:
        #     search_kwargs = {'score_threshold': 0.8}

        retriever = db.as_retriever(
            search_type='mmr',
            search_kwargs={'k': 6, 'lambda_mult': 0.25})

        return retriever
    
    def get_chromadb(self,persist_directory="../chroma_db",) -> Chroma:
        """
            returns VectorStoreRetriever using chromadb 
        """
        embedding_function = self.get_embeding_model()

        db = Chroma(persist_directory=persist_directory,
                    embedding_function=embedding_function,
                    create_collection_if_not_exists=False)

        return db
