"""
Module: message

Defines the Message model for representing individual messages in a chat session.

This module provides a Pydantic model to standardize and validate the structure
of messages exchanged between a user and an AI model. Each message includes
information about the sender's role, the content of the message, and an optional
timestamp.

Example:
    >>> from src.models.message import Message
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

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator


class Message(BaseModel):
    """
    Represents a single message in a chat session.
    
    Attributes:
        role (str): The role of the sender (e.g., "user", "assistant", "system").
        content (str): The text content of the message.
        timestamp (Optional[datetime]): The time when the message was created.
        tokens (Optional[int]): The number of tokens in the message content.
    """
    role: str  # Role of the sender (common values: "user", "assistant", "system")
    content: str  # The text content of the message
    timestamp: Optional[datetime] = None  # Timestamp of the message (optional)
    tokens: Optional[int] = None  # Number of tokens in the message content (optional)
    
    @validator('role', 'content')
    def validate_non_empty_string(cls, v):
        """
        Validates that string fields are not empty or whitespace.
        
        Args:
            v (str): The string value to validate
            
        Returns:
            str: The validated string
            
        Raises:
            ValueError: If the string is empty or only whitespace
        """
        if not v or not v.strip():
            raise ValueError("String fields cannot be empty or whitespace")
        return v
    
    @validator('tokens')
    def validate_positive_tokens(cls, v):
        """
        Validates that token count is positive if provided.
        
        Args:
            v (Optional[int]): The token count to validate
            
        Returns:
            Optional[int]: The validated token count
            
        Raises:
            ValueError: If the token count is less than or equal to 0
        """
        if v is not None and v <= 0:
            raise ValueError("Token count must be greater than 0")
        return v

    class Config:
        """
        Pydantic configuration for the Message model.
        """
        from_attributes = True  # Enables compatibility with ORMs
        validate_assignment = True  # Validate values on assignment, not just during initialization
        
    def __init__(self, **data):
        """
        Initialize a Message instance with optional automatic timestamp.
        
        If timestamp is not provided, it defaults to the current time.
        
        Args:
            **data: Data for initializing the Message instance
        """
        if 'timestamp' not in data:
            data['timestamp'] = datetime.now()
        super().__init__(**data)