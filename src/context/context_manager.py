"""
Module: context_manager

Manages the conversational context for the AI agent and delegates embedding-related tasks.
"""

from typing import List, Dict, Optional


class ContextManager:
    """
    Main class for managing the conversational context.
    """
    def __init__(self, max_messages: Optional[int] = None):
        """
        Initializes the ContextManager.

        Args:
            max_messages (Optional[int]): Maximum number of messages to retain in the context.
                                          If None, no limit is applied.
        """
        self.messages: List[Dict[str, str]] = []  # Stores the conversation history
        self.embedding_context = None  # Embedding-related operations
        self.max_messages = max_messages

    def add_message(self, role: str, content: str):
        """
        Adds a message to the conversation context.

        Args:
            role (str): The role of the speaker (e.g., "user", "assistant").
            content (str): The content of the message.

        Raises:
            ValueError: If role or content is empty.
        """
        if not role.strip():
            raise ValueError("Role cannot be empty or whitespace.")
        if not content.strip():
            raise ValueError("Content cannot be empty or whitespace.")

        self.messages.append({"role": role, "content": content})
        self._trim_messages()

    def get_recent_messages(self, n: int = 5) -> List[Dict[str, str]]:
        """
        Retrieves the most recent messages from the conversation.

        Args:
            n (int): The number of recent messages to retrieve.

        Returns:
            List[Dict[str, str]]: A list of recent messages.

        Raises:
            ValueError: If n is less than or equal to 0.
        """
        if n <= 0:
            raise ValueError("The number of messages to retrieve must be greater than 0.")
        return self.messages[-n:]

    def clear_context(self):
        """
        Clears the entire conversation context.
        """
        self.messages.clear()

    def _trim_messages(self):
        """
        Trims the message history to the maximum allowed messages, if applicable.
        """
        if self.max_messages is not None and len(self.messages) > self.max_messages:
            excess = len(self.messages) - self.max_messages
            self.messages = self.messages[excess:]
