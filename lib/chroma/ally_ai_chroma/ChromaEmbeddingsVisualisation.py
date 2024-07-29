from typing import Optional
from langchain_chroma import Chroma
from ally_ai_core.embeddings.EmbeddingsVisualisation import EmbeddingsVisualisation
import logging

class ChromaEmbeddingsVisualisation:
    def __init__(self, chroma: Chroma, limit: Optional[int] = None) -> None:
        self.chroma_client = chroma

        all_embeddings = self.get_all_embeddings(limit=limit)
        logging.info(f"Embeddings are fetched. Limit:{limit} Len:{len(all_embeddings)}")

        self._visualisation = EmbeddingsVisualisation(all_embeddings)

    def get_all_embeddings(self, limit: Optional[int] = None):
        collection = self.chroma_client.get(
            limit=limit, include=['embeddings'])
        embeddings = collection['embeddings']
        return embeddings

    def __call__(self, query):
        """
        - Makes similariy search and retrieves documents
        - Displays
            - All documents as gray dot
            - Marks query with 'red X'
            - Marks retrieved documents with 'green circle'

        """
        retrieved_documents = self.chroma_client.similarity_search(
            query=query, k=5)

        query_embeddings = self.chroma_client.embeddings.embed_query(query)
        doc_embeddings = self.chroma_client.embeddings.embed_documents(
            [doc.page_content for doc in retrieved_documents]) 
        # unfortunatelly we have to re-embed documents because we cannot fetch embedding with framework, does not support :(

        self._visualisation(
            title=query,
            query_embeddings=query_embeddings,
            document_embeddings=doc_embeddings)
