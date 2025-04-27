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
    - pickle
    - os
    - typing
    - logging
"""

import os
import pickle
import logging
from typing import List, Tuple, Optional

import numpy as np
import faiss


class FAISSManager:
    """
    Manages a FAISS index for storing and querying embeddings.
    """

    def __init__(self, dimension: int) -> None:
        """
        Initializes the FAISS manager with a flat L2 index.

        Args:
            dimension (int): The dimensionality of the embeddings.
            
        Raises:
            ValueError: If dimension is less than or equal to 0.
        """
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing FAISSManager with dimension: %d", dimension)
        
        if dimension <= 0:
            self.logger.error("Invalid dimension: %d", dimension)
            raise ValueError("Dimension must be greater than 0")
            
        self.dimension: int = dimension
        self.index: faiss.IndexFlatL2 = faiss.IndexFlatL2(dimension)  # L2 distance (Euclidean)
        self.texts: List[str] = []  # To map embeddings back to their original texts
        self.logger.info("FAISS index initialized with dimension: %d", dimension)

    def add_embeddings(self, embeddings: np.ndarray, texts: List[str]) -> None:
        """
        Adds embeddings and their corresponding texts to the FAISS index.

        Args:
            embeddings (np.ndarray): The embeddings to add (shape: [n, dimension]).
            texts (List[str]): The original texts corresponding to the embeddings.

        Raises:
            ValueError: If the number of embeddings and texts do not match.
            ValueError: If the embeddings dimension does not match the index dimension.
            ValueError: If embeddings or texts are empty.
        """
        self.logger.info("Adding %d embeddings to FAISS index", len(texts))
        
        if len(embeddings) == 0 or len(texts) == 0:
            self.logger.error("Cannot add empty embeddings or texts")
            raise ValueError("Embeddings and texts cannot be empty")
            
        if len(embeddings) != len(texts):
            self.logger.error("Number of embeddings (%d) does not match number of texts (%d)", 
                            len(embeddings), len(texts))
            raise ValueError("Number of embeddings and texts must match")
            
        if embeddings.shape[1] != self.dimension:
            self.logger.error("Embeddings dimension (%d) does not match index dimension (%d)",
                            embeddings.shape[1], self.dimension)
            raise ValueError(f"Embeddings must have dimension {self.dimension}")
        
        try:
            self.index.add(embeddings)
            self.texts.extend(texts)
            self.logger.info("Successfully added embeddings. Index now contains %d vectors", self.get_index_size())
        except Exception as e:
            self.logger.error("Error adding embeddings to FAISS index: %s", e)
            raise RuntimeError(f"Failed to add embeddings to FAISS index: {str(e)}") from e

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
            ValueError: If k is less than or equal to 0.
            RuntimeError: If search operation fails.
        """
        self.logger.info("Searching FAISS index for %d nearest neighbors", k)
        
        if k <= 0:
            self.logger.error("Invalid k value: %d", k)
            raise ValueError("k must be greater than 0")
            
        if self.get_index_size() == 0:
            self.logger.warning("Search attempted on empty index")
            return []
            
        if query_embedding.shape[1] != self.dimension:
            self.logger.error("Query dimension (%d) does not match index dimension (%d)",
                            query_embedding.shape[1], self.dimension)
            raise ValueError(f"Query embedding must have dimension {self.dimension}")
        
        try:
            k = min(k, self.get_index_size())  # Cannot retrieve more items than in the index
            distances, indices = self.index.search(query_embedding, k)
            results = [(self.texts[i], distances[0][j]) for j, i in enumerate(indices[0]) if i >= 0]
            self.logger.info("Search completed successfully, found %d results", len(results))
            return results
        except Exception as e:
            self.logger.error("Error searching FAISS index: %s", e)
            raise RuntimeError(f"Failed to search FAISS index: {str(e)}") from e

    def get_index_size(self) -> int:
        """
        Returns the number of embeddings currently stored in the FAISS index.

        Returns:
            int: The number of embeddings in the index.
        """
        self.logger.debug("Getting index size: %d", self.index.ntotal)
        return self.index.ntotal

    def reset_index(self) -> None:
        """
        Resets the FAISS index, removing all stored embeddings and texts.
        """
        self.logger.info("Resetting FAISS index")
        try:
            self.index.reset()
            self.texts.clear()
            self.logger.info("FAISS index reset successful")
        except Exception as e:
            self.logger.error("Error resetting FAISS index: %s", e)
            raise RuntimeError(f"Failed to reset FAISS index: {str(e)}") from e

    def save(self, path: str) -> None:
        """
        Saves the FAISS index and associated texts to disk for persistence.

        Args:
            path (str): The base path (without extension) to save the index and texts.
            
        Raises:
            ValueError: If path is empty or None.
            IOError: If there is an error writing to the files.
        """
        if not path or not path.strip():
            self.logger.error("Invalid save path provided")
            raise ValueError("Save path cannot be empty or None")
            
        self.logger.info("Saving FAISS index to %s.index and texts to %s.texts.pkl", path, path)
        
        try:
            faiss.write_index(self.index, path + ".index")
            with open(path + ".texts.pkl", "wb") as f:
                pickle.dump(self.texts, f)
            self.logger.info("FAISS index and texts saved successfully")
        except IOError as e:
            self.logger.error("IO error saving FAISS index or texts: %s", e)
            raise IOError(f"Error saving FAISS index or texts to {path}: {e}") from e
        except Exception as e:
            self.logger.error("Unexpected error saving FAISS index or texts: %s", e)
            raise RuntimeError(f"Unexpected error saving FAISS index to {path}: {e}") from e

    def load(self, path: str) -> None:
        """
        Loads the FAISS index and associated texts from disk.

        Args:
            path (str): The base path (without extension) to load the index and texts from.
            
        Raises:
            ValueError: If path is empty or None.
            FileNotFoundError: If index or texts file not found.
            IOError: If there is an error reading the files.
        """
        if not path or not path.strip():
            self.logger.error("Invalid load path provided")
            raise ValueError("Load path cannot be empty or None")
            
        self.logger.info("Loading FAISS index from %s.index and texts from %s.texts.pkl", path, path)
        
        try:
            if not os.path.exists(path + ".index") or not os.path.exists(path + ".texts.pkl"):
                self.logger.error("Index or texts file not found at: %s", path)
                raise FileNotFoundError("Index or texts file not found at the specified path")
                
            self.index = faiss.read_index(path + ".index")
            with open(path + ".texts.pkl", "rb") as f:
                self.texts = pickle.load(f)
                
            # Verify the loaded index has the expected dimension
            if self.index.d != self.dimension:
                self.logger.warning("Loaded index dimension (%d) differs from initialized dimension (%d)",
                                   self.index.d, self.dimension)
                self.dimension = self.index.d
                
            self.logger.info("FAISS index and texts loaded successfully. Index contains %d vectors", 
                             self.get_index_size())
        except FileNotFoundError:
            raise  # Already logged and formatted
        except IOError as e:
            self.logger.error("IO error loading FAISS index or texts: %s", e)
            raise IOError(f"Error loading FAISS index or texts from {path}: {e}") from e
        except Exception as e:
            self.logger.error("Unexpected error loading FAISS index or texts: %s", e)
            raise RuntimeError(f"Unexpected error loading FAISS index from {path}: {e}") from e
            
    def close(self) -> None:
        """
        Performs cleanup for the FAISSManager.
        
        This method is a placeholder for any cleanup logic that might be needed
        in the future for consistency with other components.
        """
        try:
            self.logger.info("Closing FAISSManager")
            # FAISS indices don't require explicit cleanup usually, but keeping for consistency
        except Exception as e:
            self.logger.error("Error during FAISSManager cleanup: %s", e)