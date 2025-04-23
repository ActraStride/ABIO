"""
Module: context_manager

Manages the conversational context for the AI agent and delegates embedding-related tasks.
"""

import numpy as np
from typing import List, Optional
from src.models.message import Message  # Import the Message model
from src.embeddings import EmbeddingsGenerator  # Import the EmbeddingsGenerator

class ContextManager:
    """
    Main class for managing the conversational context.
    """
    def __init__(
            self, 
            message_limit: Optional[int] = None, 
            context_messages: Optional[List[Message]] = None, 
            embeddings_generator: Optional[EmbeddingsGenerator] = None
        ) -> None:
        """
        Initializes the ContextManager.

        Args:
            message_limit (Optional[int]): Maximum number of messages to retain in the context.
                                          If None, no limit is applied.
            context_messages (Optional[List[Message]]): A list of pretraining messages to initialize the context.
        """
        self.messages: List[Message] = context_messages or []  # Initialize with pretraining messages
        self.message_limit = message_limit
        self.embeddings_generator = embeddings_generator or EmbeddingsGenerator()
        self.memory_embeddings = []  # Placeholder for memory embeddings

    def add_message(self, message: Message):
        """
        Adds a message to the conversation context.

        Args:
            message (Message): The message to add.

        Raises:
            ValueError: If the message is invalid.
        """
        if not message.role.strip():
            raise ValueError("Role cannot be empty or whitespace.")
        if not message.content.strip():
            raise ValueError("Content cannot be empty or whitespace.")

        self.messages.append(message)
        self._trim_messages()

    def get_recent_messages(self, n: int = 5) -> List[Message]:
        """
        Retrieves the most recent messages from the conversation.

        Args:
            n (int): The number of recent messages to retrieve.

        Returns:
            List[Message]: A list of recent messages.

        Raises:
            ValueError: If n is less than or equal to 0.
        """
        if n <= 0:
            raise ValueError("The number of messages to retrieve must be greater than 0.")
        return self.messages[-n:]

    def clear_context(self):
        """
        Clears the entire conversation context, except for the pretraining messages.
        """
        self.messages = self.messages[:len(self.messages) - len(self.messages)]

    def _trim_messages(self):
        """
        Trims the message history to the maximum allowed messages, if applicable.
        """
        if self.message_limit is not None and len(self.messages) > self.message_limit:
            excess = len(self.messages) - self.message_limit
            self.messages = self.messages[excess:]

    def add_to_memory(self, message: Message):
        """
        Adds a message to the semantic memory for future retrieval.

        Args:
            message (Message): The message to add to the memory. This message's content
                               will be converted into an embedding and stored alongside
                               the message itself.

        Raises:
            RuntimeError: If the EmbeddingsGenerator is not initialized, as it is required
                          to generate embeddings for the message content.

        Notes:
            - The message content is transformed into a vector representation (embedding)
              using the EmbeddingsGenerator.
            - The embedding and the message are stored together in the memory_embeddings list.
        """
        if self.embeddings_generator is None:
            raise RuntimeError("EmbeddingsGenerator not initialized.")
        embedding = self.embeddings_generator.generate(message.content)
        self.memory_embeddings.append((embedding, message))

    def query_memory(self, query: str, top_k: int = 1) -> List[Message]:
        """
        Searches the semantic memory for the messages most similar to the query.

        Args:
            query (str): The query string to search for in the semantic memory.
            top_k (int): The number of top similar messages to retrieve. Defaults to 1.

        Returns:
            List[Message]: A list of messages most similar to the query, sorted by similarity.

        Notes:
            - If the embeddings generator is not initialized or the memory is empty, an empty list is returned.
            - Cosine similarity is used to measure the similarity between the query and stored messages.
        """
        if self.embeddings_generator is None or not self.memory_embeddings:
            return []
        
        query_emb = self.embeddings_generator.generate(query)
        
        # Compute cosine similarity between the query embedding and memory embeddings
        sims = [
            (np.dot(query_emb, emb.T) / (np.linalg.norm(query_emb) * np.linalg.norm(emb)), msg)
            for emb, msg in self.memory_embeddings
        ]
        
        # Sort by similarity score in descending order
        sims.sort(reverse=True, key=lambda x: x[0])
        
        # Return the top_k most similar messages
        return [msg for _, msg in sims[:top_k]]
