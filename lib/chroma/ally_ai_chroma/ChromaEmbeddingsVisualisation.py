from typing import Literal, Optional
from .Chroma import Chroma
from ally_ai_core.embeddings.EmbeddingsVisualisation import EmbeddingsVisualisation
import logging
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
logger = logging.getLogger(__name__)


class ChromaEmbeddingsVisualisation:
    def __init__(self, chroma: Chroma, limit: Optional[int] = None) -> None:
        logger.info("init is called.")

        self.chroma_client = chroma
        all_embeddings = self.get_all_embeddings(limit=limit)
        self._visualisation = EmbeddingsVisualisation(all_embeddings)

    def get_all_embeddings(self, limit: Optional[int] = None):
        logger.info("fetching embeddings is starting...")

        collection = self.chroma_client.get(
            limit=limit, include=['embeddings'])
        embeddings = collection['embeddings']
        
        logger.info(f"fetching embeddings is done. Len:{len(embeddings)}")
        return embeddings

    def __call__(self, query, search_type: Literal['similarity', 'mmr', 'similarity_score_threshold']='mmr', **kwargs):
        """
        - Makes similariy search and retrieves documents
        - Displays
            - All documents as gray dot
            - Marks query with 'red X'
            - Marks retrieved documents with 'green circle'

        """
        retrieved_documents = self.chroma_client.search(query=query, search_type=search_type, **kwargs)

        query_embeddings = self.chroma_client.embeddings.embed_query(query)
        doc_embeddings = self.chroma_client.embeddings.embed_documents(
            [doc.page_content for doc in retrieved_documents]) 
        # unfortunatelly we have to re-embed documents because we cannot fetch embedding with framework, does not support :(

        self._visualisation(
            title=query,
            query_embeddings=query_embeddings,
            document_embeddings=doc_embeddings)
