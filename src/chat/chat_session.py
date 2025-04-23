"""
Module: chat_session

Defines the ChatSession class for managing conversational interactions
between a user and an AI model.

This module provides a structure for handling chat sessions, including the storage
of message history, context management, and interaction with AI models.

Example:
    >>> from src.chat.chat_session import ChatSession
    >>> from src.models.message import Message
    >>> session = ChatSession(session_id="12345", client=gemini_client_instance)
    >>> session.add_message(role="user", content="Hello!")
    >>> response = session.generate_response()
    >>> print(response.content)

Dependencies:
    - typing
    - datetime
    - src.models.message
"""

from typing import List
from src.models import Message  # Import Message from the models module
from src.clients.gemini_client import GeminiClient
from src.context.context_manager import ContextManager  # Import ContextManager
import logging

class ChatSession:
    """
    Manages a chat session, including message history and interactions with an AI model.

    """
    def __init__(self, session_id: str, client: GeminiClient, context_manager: ContextManager):
        """
        Initializes a new ChatSession.

        Args:
            session_id (str): A unique identifier for the session.
            client (GeminiClient): The client used to interact with the AI model.
        """
        self.logger = logging.getLogger(__name__)  # Create a logger for this class
        self.logger.info("Initializing ChatSession with session_id: %s", session_id)
        self.session_id = session_id  # Unique identifier for the session
        self.client = client
        self.context_manager = context_manager # Initialize ContextManager
        self._initialize_context()


    
    def _initialize_context(self):
        """
        Initializes the model context with the full message history.
        Concatenates all messages' content and sends it to the model as a single string.
        """
        self.logger.info("Initializing context with existing message history.")

        if not self.context_manager.messages:
            self.logger.warning("No messages found in context manager during initialization.")
            return

        # Concatenate all message contents into a single string
        full_context = "\n".join(
            f"{msg.role}: {msg.content}" for msg in self.context_manager.messages
        )

        # Send the full context to the model
        self.generate_response(full_context)


    def add_message(self, role: str, content: str) -> None:
        """
        Adds a new message to the session.

        Args:
            role (str): The role of the sender (e.g., "user", "assistant", "system").
            content (str): The text content of the message.
        """
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
        Generates a response using the AI model via the client.

        Args:
            prompt (str): The input prompt for the AI model.

        Returns:
            Message: The AI-generated response as a Message object.
        """
        self.logger.info("Generating response for prompt: %s", prompt)

        # Retrieve the conversation history
        history = self.get_history()
        history_text = "\n".join(
            f"{message.role.capitalize()}: {message.content}" for message in history
        )

        # Combine history with the current prompt
        full_prompt = f"{history_text}\nUser: {prompt}"

        # Generate response using the AI model
        response = self.client.generate_text(prompt=full_prompt)
        generated_text = response.generated_text if hasattr(response, "generated_text") else "Error: No se pudo generar una respuesta."
        self.logger.info("Generated response: %s", generated_text)

        # Create a Message object for the response
        response_message = Message(role="assistant", content=generated_text)
        self.add_message(role="assistant", content=generated_text)

        return response_message