"""
Module: config

Defines the configuration models for the Abio AI agent.

This module provides Pydantic models to structure, validate, and manage
configuration data loaded from an Abiofile (YAML or JSON). The configuration
includes agent metadata, chat settings, context settings, and initial context messages.

Example:
    >>> from src.models.config import AbioConfig
    >>> config = AbioConfig.parse_file("abiofile.yaml")
    >>> print(config.agent.name)

Dependencies:
    - pydantic
    - typing
    - datetime
"""

from pydantic import BaseModel, Field
from typing import List, Literal, Optional
from datetime import datetime
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

    class Config:
        from_attributes = True


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

    class Config:
        from_attributes = True


class ContextConfig(BaseModel):
    """
    Configuration for managing conversation context, including history size
    and initial context messages.

    Attributes:
        message_limit (int): Maximum number of messages to retain in the context history.
        context_messages (List[ContextMessage]): List of context messages to start the context.
    """
    message_limit: int = Field(..., ge=1)
    context_messages: List[Message] = []

    class Config:
        from_attributes = True


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

    class Config:
        from_attributes = True


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
        from_attributes = True