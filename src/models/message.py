"""
Module: message

Defines the Message model for representing individual messages in a chat session.

This module provides a Pydantic model to standardize and validate the structure
of messages exchanged between a user and an AI model. Each message includes
information about the sender's role, the content of the message, and an optional
timestamp.

Example:
    >>> from src.models import Message
    >>> message = Message(
    ...     role="user",
    ...     content="Hello, how are you?",
    ...     timestamp="2025-04-03T12:34:56"
    ... )
    >>> print(message.content)

Dependencies:
    - pydantic
    - typing
    - datetime
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Message(BaseModel):
    """
    Represents a single message in a chat session.
    
    Attributes:
        role (str): The role of the sender (e.g., "user", "assistant", "system").
        content (str): The text content of the message.
        timestamp (Optional[datetime]): The time when the message was created.
        tokens (Optional[int]): The number of tokens in the message content.
    """
    # TODO - Enhance role management with an Enum for better validation
    # REVIEW -  - Add role model to manage roles?
    role: str  # Role of the sender (common values: "user", "assistant", "system")
    content: str  # The text content of the message
    timestamp: Optional[datetime] = None  # Timestamp of the message (optional)
    tokens: Optional[int] = None  # Number of tokens in the message content (optional)

    class Config:
        """
        Pydantic configuration for the Message model.
        """
        from_attributes = True  # Enables compatibility with ORMs