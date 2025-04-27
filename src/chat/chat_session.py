"""
Module: chat_session

Defines the ChatSession class for managing conversational interactions
between a user and an AI model.

This module provides a structure for handling chat sessions, including the storage
of message history, context management, and interaction with AI models.

Example:
    >>> from src.chat.chat_session import ChatSession
    >>> from src.clients.gemini_client import GeminiClient
    >>> from src.context.context_manager import ContextManager
    >>> from src.models.message import Message
    >>> client = GeminiClient()
    >>> context_manager = ContextManager()
    >>> session = ChatSession(session_id="12345", client=client, context_manager=context_manager)
    >>> session.add_message(role="user", content="Hello!")
    >>> response = session.generate_response("Hello!")
    >>> print(response.content)

Dependencies:
    - typing
    - logging
    - src.models.message
    - src.clients.gemini_client
    - src.context.context_manager
    - src.embeddings.embeddings_generator
"""

from typing import List, Optional
import logging

from src.models.message import Message  # Correct import path
from src.clients.gemini_client import GeminiClient
from src.context.context_manager import ContextManager
from src.embeddings.embeddings_generator import EmbeddingsGenerator

class ChatSession:
    """
    Manages a chat session, including message history and interactions with an AI model.
    """

    def __init__(
        self, 
        session_id: str, 
        client: GeminiClient, 
        context_manager: ContextManager,
        embeddings_generator: Optional[EmbeddingsGenerator] = None
    ):
        """
        Initializes a new ChatSession.

        Args:
            session_id (str): A unique identifier for the session.
            client (GeminiClient): The client used to interact with the AI model.
            context_manager (ContextManager): Manages the context and message history.
            embeddings_generator (EmbeddingsGenerator, optional): For embedding operations.
            
        Raises:
            ValueError: If session_id is empty or client/context_manager is None.
        """
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing ChatSession with session_id: %s", session_id)
        
        # Validate inputs
        if not session_id.strip():
            self.logger.error("Empty session_id provided.")
            raise ValueError("session_id cannot be empty or whitespace.")
        if client is None:
            self.logger.error("No client provided.")
            raise ValueError("client must be provided.")
        if context_manager is None:
            self.logger.error("No context_manager provided.")
            raise ValueError("context_manager must be provided.")
            
        self.session_id = session_id
        self.client = client
        self.context_manager = context_manager
        self.embeddings_generator = embeddings_generator

    def add_message(self, role: str, content: str) -> None:
        """
        Adds a new message to the session.

        Args:
            role (str): The role of the sender (e.g., "user", "assistant", "system").
            content (str): The text content of the message.
            
        Raises:
            ValueError: If role or content is empty.
        """
        if not role.strip():
            self.logger.error("Empty role provided.")
            raise ValueError("role cannot be empty or whitespace.")
        if not content.strip():
            self.logger.error("Empty content provided.")
            raise ValueError("content cannot be empty or whitespace.")
            
        self.logger.debug("Adding message with role: %s, content: %s", role, content)
        message = Message(role=role, content=content)
        self.context_manager.add_message(message)

    def get_history(self) -> List[Message]:
        """
        Retrieves the message history of the session.

        Returns:
            List[Message]: A list of all messages in the session.
        """
        self.logger.debug("Retrieving message history.")
        return self.context_manager.messages

    def generate_response(self, prompt: str) -> Message:
        """
        Generates a response using the AI model based on the prompt and conversation history.

        Args:
            prompt (str): The latest user input to respond to.

        Returns:
            Message: The AI-generated response as a Message object.
            
        Raises:
            ValueError: If prompt is empty.
            RuntimeError: If response generation fails.
        """
        if not prompt.strip():
            self.logger.error("Empty prompt provided.")
            raise ValueError("prompt cannot be empty or whitespace.")
            
        self.logger.info("Generating response for prompt: %s", prompt)

        try:
            # Retrieve the conversation history
            history = self.get_history()
            history_text = "\n".join(
                f"{message.role.capitalize()}: {message.content}" for message in history
            )

            # Combine history with the current prompt
            full_prompt = f"{history_text}\nUser: {prompt}"

            # Generate response using the AI model
            response = self.client.generate_text(prompt=full_prompt)
            
            if not hasattr(response, "generated_text") or not response.generated_text:
                self.logger.error("Failed to get valid response from model.")
                raise RuntimeError("Model returned an invalid response.")
                
            generated_text = response.generated_text
            self.logger.info("Generated response: %s", generated_text)

            # Create a Message object for the response
            response_message = Message(role="assistant", content=generated_text)
            self.context_manager.add_message(response_message)

            return response_message
            
        except Exception as e:
            self.logger.error("Error generating response: %s", e)
            raise RuntimeError(f"Failed to generate response: {str(e)}") from e
            
    def close(self) -> None:
        """
        Performs cleanup for the ChatSession.
        
        Closes any resources used by the session.
        """
        try:
            self.logger.info("Closing ChatSession with session_id: %s", self.session_id)
            if self.client:
                self.client.close()
            # Add any other cleanup as needed
        except Exception as e:
            self.logger.error("Error during ChatSession cleanup: %s", e)