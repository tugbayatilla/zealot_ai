from typing import List
import umap
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt


class EmbeddingsVisualisation:
    def __init__(self, all_embeddings) -> None:

        self.all_embeddings = all_embeddings
        self._all_embeddings_2d = None
        self.umap_transform = self.get_umap_transform()

    def get_umap_transform(self, random_state=0, transform_seed=0):
        umap_transform = umap.UMAP(
            random_state=random_state, transform_seed=transform_seed).fit(self.all_embeddings)
        return umap_transform

    def convert_embeddings_to_2D(self, embeddings):
        umap_embeddings = np.empty((len(embeddings), 2))
        for i, embedding in enumerate(tqdm(embeddings)):
            umap_embeddings[i] = self.umap_transform.transform([embedding])
        return umap_embeddings

    def __call__(self, title: str, query_embeddings: List[float], document_embeddings: List[List[float]]) -> None:
        self.visualise(
            title=title,
            query_embeddings=query_embeddings,
            document_embeddings=document_embeddings)

    def visualise(self, title: str, query_embeddings: List[float], document_embeddings: List[List[float]]) -> None:
        """
        - Makes similariy search and retrieves documents
        - Displays
            - All documents as gray dot
            - Marks query with 'red X'
            - Marks retrieved documents with 'green circle'

        """

        if self._all_embeddings_2d is None:
            self._all_embeddings_2d = self.convert_embeddings_to_2D(
                self.all_embeddings)

        query_embeddings_2d = self.convert_embeddings_to_2D([query_embeddings])
        document_embeddings_2d = self.convert_embeddings_to_2D(
            document_embeddings)

        # Plot the projected query and retrieved documents in the embedding space
        plt.figure()
        plt.scatter(
            self._all_embeddings_2d[:, 0], self._all_embeddings_2d[:, 1], s=10, color='gray')
        plt.scatter(
            query_embeddings_2d[:, 0], query_embeddings_2d[:, 1], s=150, marker='X', color='r')
        plt.scatter(
            document_embeddings_2d[:, 0], document_embeddings_2d[:, 1], s=100, facecolors='none', edgecolors='g')

        plt.gca().set_aspect('equal', 'datalim')
        plt.title(f'{title}')
        plt.axis('off')
