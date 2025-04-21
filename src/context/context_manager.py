"""
Module: context_manager

Manages the conversational context for the AI agent and delegates embedding-related tasks.
"""

from typing import List, Optional
from src.models.message import Message  # Import the Message model

class ContextManager:
    """
    Main class for managing the conversational context.
    """
    def __init__(self, message_limit: Optional[int] = None, context_messages: Optional[List[Message]] = None):
        """
        Initializes the ContextManager.

        Args:
            message_limit (Optional[int]): Maximum number of messages to retain in the context.
                                          If None, no limit is applied.
            context_messages (Optional[List[Message]]): A list of pretraining messages to initialize the context.
        """
        self.messages: List[Message] = context_messages or []  # Initialize with pretraining messages
        print(f"ContextManager {self.messages}.")
        self.embedding_context = None  # Embedding-related operations
        self.message_limit = message_limit

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
