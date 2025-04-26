"""
Module: faiss_manager

Provides functionality for managing a FAISS index to store and query embeddings.
This module is useful for efficient similarity search and nearest neighbor retrieval.

Example:
    >>> from src.faiss.faiss_manager import FAISSManager
    >>> manager = FAISSManager(dimension=384)
    >>> embeddings = np.random.rand(10, 384).astype('float32')
    >>> texts = [f"Text {i}" for i in range(10)]
    >>> manager.add_embeddings(embeddings, texts)
    >>> query = embeddings[0:1]
    >>> results = manager.search(query, k=3)
    >>> print(results)

Dependencies:
    - faiss
    - numpy
    - typing
"""

import faiss
import numpy as np
import pickle
import os
from typing import List, Tuple


class FAISSManager:
    """
    Manages a FAISS index for storing and querying embeddings.
    """

    def __init__(self, dimension: int) -> None:
        """
        Initializes the FAISS manager with a flat L2 index.

        Args:
            dimension (int): The dimensionality of the embeddings.
        """
        self.dimension: int = dimension
        self.index: faiss.IndexFlatL2 = faiss.IndexFlatL2(dimension)  # L2 distance (Euclidean)
        self.texts: List[str] = []  # To map embeddings back to their original texts

    def add_embeddings(self, embeddings: np.ndarray, texts: List[str]) -> None:
        """
        Adds embeddings and their corresponding texts to the FAISS index.

        Args:
            embeddings (np.ndarray): The embeddings to add (shape: [n, dimension]).
            texts (List[str]): The original texts corresponding to the embeddings.

        Raises:
            ValueError: If the number of embeddings and texts do not match.
        """
        if len(embeddings) != len(texts):
            raise ValueError("Number of embeddings and texts must match.")
        if embeddings.shape[1] != self.dimension:
            raise ValueError(f"Embeddings must have dimension {self.dimension}.")
        
        self.index.add(embeddings)
        self.texts.extend(texts)

    def search(self, query_embedding: np.ndarray, k: int = 5) -> List[Tuple[str, float]]:
        """
        Searches for the k most similar embeddings in the FAISS index.

        Args:
            query_embedding (np.ndarray): The embedding to search for (shape: [1, dimension]).
            k (int): The number of nearest neighbors to retrieve.

        Returns:
            List[Tuple[str, float]]: A list of tuples (text, distance) for the top-k results.

        Raises:
            ValueError: If the query embedding does not match the index dimension.
        """
        if query_embedding.shape[1] != self.dimension:
            raise ValueError(f"Query embedding must have dimension {self.dimension}.")
        
        distances, indices = self.index.search(query_embedding, k)
        return [(self.texts[i], distances[0][j]) for j, i in enumerate(indices[0])]

    def get_index_size(self) -> int:
        """
        Returns the number of embeddings currently stored in the FAISS index.

        Returns:
            int: The number of embeddings in the index.
        """
        return self.index.ntotal

    def reset_index(self) -> None:
        """
        Resets the FAISS index, removing all stored embeddings and texts.
        """
        self.index.reset()
        self.texts.clear()

    def save(self, path: str) -> None:
        """
        Saves the FAISS index and associated texts to disk for persistence.

        Args:
            path (str): The base path (without extension) to save the index and texts.
        """
        faiss.write_index(self.index, path + ".index")
        with open(path + ".texts.pkl", "wb") as f:
            pickle.dump(self.texts, f)

    def load(self, path: str) -> None:
        """
        Loads the FAISS index and associated texts from disk.

        Args:
            path (str): The base path (without extension) to load the index and texts from.
        """
        if not os.path.exists(path + ".index") or not os.path.exists(path + ".texts.pkl"):
            raise FileNotFoundError("Index or texts file not found at the specified path.")
        self.index = faiss.read_index(path + ".index")
        with open(path + ".texts.pkl", "rb") as f:
            self.texts = pickle.load(f)