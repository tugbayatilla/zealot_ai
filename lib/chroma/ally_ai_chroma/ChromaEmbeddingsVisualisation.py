from typing import Literal, Optional

from matplotlib.figure import Figure
from .Chroma import Chroma
from ally_ai_core.embeddings.EmbeddingsVisualisation import EmbeddingsVisualisation
import logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
logger = logging.getLogger(__name__)


class ChromaEmbeddingsVisualisation:
    def __init__(self, chroma: Chroma, limit: Optional[int] = None) -> None:
        logger.info("init is called.")

        self.chroma_client = chroma
        self.document_embeddings, self.documents = self.get_documents_and_embeddings(
            limit=limit)
        self.visualisation = EmbeddingsVisualisation(
            self.document_embeddings)

    def get_documents_and_embeddings(self, limit: Optional[int] = None):
        include = ['embeddings', 'documents']
        logger.info(f"getting data '{include}' from chroma client")

        collection = self.chroma_client.get(limit=limit, include=include)
        document_embeddings = collection['embeddings']
        documents = collection['documents']

        logger.info(f"total documents: {len(documents)}")
        return (document_embeddings, documents)

    def __call__(self, query, search_type: Literal['similarity', 'mmr', 'similarity_score_threshold'] = 'mmr', **kwargs) -> Figure:
        """
        - Makes similariy search and retrieves documents
        - Displays
            - All documents as gray dot
            - Marks query with 'red X'
            - Marks retrieved documents with 'green circle'

        """
        logger.info(f"retrieving documents. Query: {query}")
        retrieved_documents = self.chroma_client.search(
            query=query, search_type=search_type, **kwargs)

        logger.info(f"embedding the query. Query: {query}")
        query_embeddings = self.chroma_client.embeddings.embed_query(query)

        return self.visualisation(
            title=query,
            query_embeddings=query_embeddings,
            document_embeddings=retrieved_documents)
