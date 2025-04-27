"""
Module: context_manager

Manages the conversational context for the AI agent, including message history
and context window management.

This module provides functionality for:
- Adding messages to the conversation context
- Retrieving recent messages
- Managing context window size through message limits
- Clearing conversation history

Example:
    >>> from src.context.context_manager import ContextManager
    >>> from src.models.message import Message
    >>> context = ContextManager(message_limit=10)
    >>> context.add_message(Message(role="user", content="Hello!"))
    >>> context.add_message(Message(role="assistant", content="Hi there!"))
    >>> recent_messages = context.get_recent_messages(n=2)
    >>> for msg in recent_messages:
    >>>     print(f"{msg.role}: {msg.content}")

Dependencies:
    - typing
    - logging
    - src.models.message
"""

import logging
from typing import List, Optional

from src.models.message import Message

class ContextManager:
    """
    Main class for managing the conversational context and message history.
    """
    def __init__(
            self, 
            message_limit: Optional[int] = None, 
            context_messages: Optional[List[Message]] = None, 
        ) -> None:
        """
        Initializes the ContextManager.

        Args:
            message_limit (Optional[int]): Maximum number of messages to retain in the context.
                                          If None, no limit is applied.
            context_messages (Optional[List[Message]]): A list of pretraining messages to initialize the context.
        """
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing ContextManager with message_limit: %s", message_limit)
        
        self.messages: List[Message] = context_messages or []  # Initialize with pretraining messages
        self.message_limit = message_limit
        
        if context_messages:
            self.logger.info("Context initialized with %d existing messages", len(context_messages))

    def add_message(self, message: Message) -> None:
        """
        Adds a message to the conversation context.

        Args:
            message (Message): The message to add.

        Raises:
            ValueError: If the message is invalid.
        """
        if not message.role.strip():
            self.logger.error("Cannot add message with empty role.")
            raise ValueError("Role cannot be empty or whitespace.")
        if not message.content.strip():
            self.logger.error("Cannot add message with empty content.")
            raise ValueError("Content cannot be empty or whitespace.")

        self.logger.debug("Adding message with role: %s, content: %s", message.role, message.content)
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
            self.logger.error("Invalid number of messages requested: %d", n)
            raise ValueError("The number of messages to retrieve must be greater than 0.")
            
        self.logger.debug("Retrieving %d recent messages.", n)
        return self.messages[-n:]

    def clear_context(self) -> None:
        """
        Clears the entire conversation context.
        """
        self.logger.info("Clearing all messages from context.")
        self.messages = []

    def _trim_messages(self) -> None:
        """
        Trims the message history to the maximum allowed messages, if applicable.
        """
        if self.message_limit is not None and len(self.messages) > self.message_limit:
            excess = len(self.messages) - self.message_limit
            self.logger.debug("Trimming %d excess messages from context.", excess)
            self.messages = self.messages[excess:]
            
    def close(self) -> None:
        """
        Performs cleanup for the ContextManager.
        
        This method is a placeholder for any cleanup logic that might be needed
        in the future for consistency with other components.
        """
        try:
            self.logger.info("Closing ContextManager.")
            # Add any cleanup logic here if needed in the future
        except Exception as e:
            self.logger.error("Error during ContextManager cleanup: %s", e)

