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
"""

from sentence_transformers import SentenceTransformer
from typing import List, Union, Optional
import numpy as np


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
        """
        self.model_name: str = model_name
        self.model: SentenceTransformer = SentenceTransformer(model_name)
        # Vector space dimension (specific to the model)
        self.dimension: int = self.model.get_sentence_embedding_dimension()
    
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
        """
        return self.model.encode(text, batch_size=batch_size)
    
    def get_dimension(self) -> int:
        """
        Returns the dimension of the model's vector space.
        
        Returns:
            int: The dimension of the generated vectors.
        """
        return self.dimension
    
    def preprocess_text(self, text: str) -> str:
        """
        Preprocesses text before generating embeddings.
        
        Args:
            text (str): Text to preprocess
            
        Returns:
            str: Preprocessed text
        """
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
        """
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
            
        return segments