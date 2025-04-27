"""
Module: embeddings_generator

Provides functionality for generating embeddings from text using SentenceTransformers.
These embeddings are vector representations that capture semantic meaning of text,
useful for similarity comparisons, clustering, and other NLP tasks.

Example:
    >>> from src.embeddings.embeddings_generator import EmbeddingsGenerator
    >>> generator = EmbeddingsGenerator()
    >>> embeddings = generator.generate("Hello world")
    >>> print(f"Embedding dimension: {generator.get_dimension()}")

Dependencies:
    - sentence_transformers
    - numpy
    - typing
    - logging
"""

import logging
from typing import List, Union, Optional
import numpy as np
from sentence_transformers import SentenceTransformer


class EmbeddingsGenerator:
    """
    Generates embeddings using SentenceTransformers models.
    Transforms text into vector representations that capture semantic meaning.
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2") -> None:
        """
        Initializes the embeddings generator with a specific model.
        
        Args:
            model_name (str): Name of the SentenceTransformer model to use.
                Default is all-MiniLM-L6-v2 (384 dimensions).
                
        Raises:
            RuntimeError: If the model fails to load.
        """
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing EmbeddingsGenerator with model: %s", model_name)
        
        self.model_name: str = model_name
        try:
            self.model: SentenceTransformer = SentenceTransformer(model_name)
            # Vector space dimension (specific to the model)
            self.dimension: int = self.model.get_sentence_embedding_dimension()
            self.logger.info("Model loaded successfully. Embedding dimension: %d", self.dimension)
        except Exception as e:
            self.logger.error("Failed to load embedding model %s: %s", model_name, e)
            raise RuntimeError(f"Failed to load embedding model {model_name}") from e
    
    def generate(self, text: Union[str, List[str]], 
                 batch_size: int = 32) -> np.ndarray:
        """
        Generates embeddings for a text or list of texts.
        
        Args:
            text (Union[str, List[str]]): A string or list of strings to vectorize
            batch_size (int): Batch size for efficient processing
            
        Returns:
            np.ndarray: NumPy array with generated embeddings. If input is a single
                text, returns a 1D vector. If it's a list, returns a 2D matrix.
                
        Raises:
            ValueError: If text is empty or None.
            RuntimeError: If embedding generation fails.
        """
        if text is None:
            self.logger.error("Cannot generate embeddings for None")
            raise ValueError("Text cannot be None")
        
        if isinstance(text, str) and not text.strip():
            self.logger.error("Cannot generate embeddings for empty text")
            raise ValueError("Text cannot be empty or whitespace")
            
        if isinstance(text, list) and (not text or all(not t.strip() for t in text if isinstance(t, str))):
            self.logger.error("Cannot generate embeddings for empty list or list with empty strings")
            raise ValueError("Text list cannot be empty or contain only empty strings")
            
        if batch_size <= 0:
            self.logger.error("Invalid batch size: %d", batch_size)
            raise ValueError("Batch size must be greater than 0")
        
        self.logger.debug("Generating embeddings for %s", 
                          f"{len(text)} texts" if isinstance(text, list) else "1 text")
        try:
            result = self.model.encode(text, batch_size=batch_size)
            self.logger.debug("Successfully generated embeddings with shape %s", result.shape)
            return result
        except Exception as e:
            self.logger.error("Error generating embeddings: %s", e)
            raise RuntimeError("Failed to generate embeddings") from e
    
    def get_dimension(self) -> int:
        """
        Returns the dimension of the model's vector space.
        
        Returns:
            int: The dimension of the generated vectors.
        """
        self.logger.debug("Returning embedding dimension: %d", self.dimension)
        return self.dimension
    
    def preprocess_text(self, text: str) -> str:
        """
        Preprocesses text before generating embeddings.
        
        Args:
            text (str): Text to preprocess
            
        Returns:
            str: Preprocessed text
            
        Raises:
            ValueError: If text is None or empty.
        """
        if text is None:
            self.logger.error("Cannot preprocess None text")
            raise ValueError("Text cannot be None")
            
        if not text.strip():
            self.logger.error("Cannot preprocess empty text")
            raise ValueError("Text cannot be empty or whitespace")
            
        self.logger.debug("Preprocessing text")
        # Basic preprocessing - can be expanded based on needs
        text = text.strip()
        # Optional: normalization, special character removal, etc.
        return text
    
    def segment_text(self, text: str, max_length: int = 512) -> List[str]:
        """
        Segments long texts into more manageable chunks.
        
        Args:
            text (str): Long text to segment
            max_length (int): Maximum approximate length per segment
            
        Returns:
            List[str]: List of text segments
            
        Raises:
            ValueError: If text is None or empty, or if max_length is invalid.
        """
        if text is None:
            self.logger.error("Cannot segment None text")
            raise ValueError("Text cannot be None")
            
        if not text.strip():
            self.logger.error("Cannot segment empty text")
            raise ValueError("Text cannot be empty or whitespace")
            
        if max_length <= 0:
            self.logger.error("Invalid max_length: %d", max_length)
            raise ValueError("max_length must be greater than 0")
            
        self.logger.debug("Segmenting text with max_length: %d", max_length)
        
        # Basic implementation - can be improved with more sophisticated techniques
        # that maintain context or semantic divisions
        words = text.split()
        segments = []
        current_segment = []
        
        for word in words:
            current_segment.append(word)
            if len(' '.join(current_segment)) >= max_length:
                segments.append(' '.join(current_segment))
                current_segment = []
                
        if current_segment:
            segments.append(' '.join(current_segment))
            
        self.logger.debug("Text segmented into %d chunks", len(segments))
        return segments
    
    def close(self) -> None:
        """
        Performs cleanup for the EmbeddingsGenerator.
        
        This method releases resources associated with the model when no longer needed.
        """
        try:
            self.logger.info("Closing EmbeddingsGenerator.")
            # If any cleanup is needed for the SentenceTransformer model
            # For example, clearing CUDA memory if applicable
            if hasattr(self, 'model') and self.model is not None:
                # Most models don't require explicit cleanup, but adding placeholder
                # for consistency with other components
                pass
        except Exception as e:
            self.logger.error("Error during EmbeddingsGenerator cleanup: %s", e)