"""
Module Name: agent_config

Configuration module for defining the initial state and behavior of an AI agent.

This module provides a class, `AgentConfig`, which encapsulates the configuration
parameters required to initialize and manage the behavior of an AI agent. It includes
attributes such as the agent's name, role, pretraining prompts, and other contextual
settings.

Example:
    >>> from src.config.agent_config import AgentConfig
    >>> config = AgentConfig(
    ...     name="Assistant",
    ...     role="Helpful assistant",
    ...     pretraining_prompts=["How can I assist you today?"],
    ...     context="General knowledge",
    ...     max_messages=100,
    ...     temperature=0.8
    ... )
    >>> print(config.name)

Dependencies:
    - json
    - typing (List, Optional)
"""

from typing import List, Optional
import json

class AgentConfig:
    """
    A configuration class for defining the initial state and behavior of the AI agent.

    """

    def __init__(
        self,
        name: str,
        role: str,
        pretraining_prompts: List[str],
        context: Optional[str] = None,
        max_messages: int = 50,
        temperature: float = 0.7,
    ):
        """
        Initializes an instance of the AgentConfig class.

        Args:
            name (str): The name of the agent.
            role (str): The primary role or persona of the agent.
            pretraining_prompts (List[str]): A list of prompts used to pretrain or initialize the agent's behavior.
            context (Optional[str], optional): An optional initial context or background information for the agent. Defaults to None.
            max_messages (int, optional): The maximum number of messages to retain in the agent's context history. Defaults to 50.
            temperature (float, optional): A parameter controlling the randomness or creativity of the AI model's responses. Defaults to 0.7.
        """
        self.name = name
        self.role = role
        self.pretraining_prompts = pretraining_prompts
        self.context = context
        self.max_messages = max_messages
        self.temperature = temperature
