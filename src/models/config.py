"""
Module: config

Defines the configuration models for the Abio AI agent.

This module provides Pydantic models to structure, validate, and manage
configuration data loaded from an Abiofile (YAML or JSON). The configuration
includes agent metadata, chat settings, context settings, and initial context messages.

Example:
    >>> from src.models.config import AbioConfig
    >>> config = AbioConfig.model_validate_json(open("abiofile.json").read())
    >>> print(config.agent.name)

Dependencies:
    - pydantic
    - typing
    - datetime
    - src.models.message
"""

from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, Field, validator

from src.models.message import Message


class AgentConfig(BaseModel):
    """
    Configuration for the AI agent.

    Attributes:
        name (str): Name of the agent.
        version (str): Agent version (e.g., 1.0.0).
        description (str): Short description of the agent.
        environment (Literal): Runtime environment.
    """
    name: str
    version: str
    description: str
    environment: Literal["development", "production", "test"]

    @validator('name', 'description')
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
        
    @validator('version')
    def validate_version_format(cls, v):
        """
        Validates that version follows semantic versioning format.
        
        Args:
            v (str): The version string to validate
            
        Returns:
            str: The validated version string
            
        Raises:
            ValueError: If the version string is improperly formatted
        """
        if not v or not v.strip():
            raise ValueError("Version cannot be empty or whitespace")
        
        # Simple validation for version format (can be extended)
        parts = v.split('.')
        if len(parts) < 2:
            raise ValueError("Version should follow semantic versioning (e.g., 1.0.0)")
        return v

    class Config:
        """Pydantic configuration for AgentConfig"""
        from_attributes = True
        validate_assignment = True


class ChatConfig(BaseModel):
    """
    Configuration related to chat behavior and model parameters,
    excluding context management.

    Attributes:
        default_model (str): Name of the default model.
        temperature (float): Sampling temperature.
        top_p (float): Nucleus sampling value.
    """
    default_model: str
    temperature: float = Field(..., ge=0.0, le=1.0)
    top_p: float = Field(..., ge=0.0, le=1.0)

    @validator('default_model')
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
            raise ValueError("Model name cannot be empty or whitespace")
        return v

    class Config:
        """Pydantic configuration for ChatConfig"""
        from_attributes = True
        validate_assignment = True


class ContextConfig(BaseModel):
    """
    Configuration for managing conversation context, including history size
    and initial context messages.

    Attributes:
        message_limit (int): Maximum number of messages to retain in the context history.
        context_messages (List[Message]): List of messages to initialize the context.
    """
    message_limit: int = Field(..., ge=1)
    context_messages: List[Message] = []

    class Config:
        """Pydantic configuration for ContextConfig"""
        from_attributes = True
        validate_assignment = True


class MetaConfig(BaseModel):
    """
    Metadata for configuration creation and versioning.

    Attributes:
        created_by (str): Author of the configuration.
        created_at (str): ISO date of creation.
        last_updated (str): ISO date of last update.
    """
    created_by: str
    created_at: str
    last_updated: str

    @validator('created_by')
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
            raise ValueError("Author name cannot be empty or whitespace")
        return v
        
    @validator('created_at', 'last_updated')
    def validate_date_format(cls, v):
        """
        Validates date strings are in YYYY-MM-DD format.
        
        Args:
            v (str): The date string to validate
            
        Returns:
            str: The validated date string
            
        Raises:
            ValueError: If the date string is improperly formatted
        """
        if not v or not v.strip():
            raise ValueError("Date cannot be empty or whitespace")
        
        try:
            # Attempt to parse the date
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")
        return v

    class Config:
        """Pydantic configuration for MetaConfig"""
        from_attributes = True
        validate_assignment = True


class AbioConfig(BaseModel):
    """
    Root configuration model for the Abio agent.

    Attributes:
        agent (AgentConfig): General info and runtime environment.
        chat (ChatConfig): Chat parameters related to model behavior.
        context (ContextConfig): Configuration for managing conversation context.
        meta (MetaConfig): Metadata about the config file.
    """
    agent: AgentConfig
    chat: ChatConfig
    context: ContextConfig
    meta: MetaConfig

    class Config:
        """Pydantic configuration for AbioConfig"""
        from_attributes = True
        validate_assignment = True