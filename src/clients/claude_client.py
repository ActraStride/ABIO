"""
Module Name: claude_client

Client for interacting with the Claude generative AI service.

This module provides a wrapper around the Anthropic SDK, enabling:
- Configuration of the Claude API with an API key.
- Retrieval of available models for content generation.
- Text generation using a specified model.

Example:
    >>> from src.clients.claude_client import ClaudeClient
    >>> client = ClaudeClient(api_key="your_api_key")
    >>> response = client.generate_text(prompt="Hello, Claude!")
    >>> print(response)

Dependencies:
    - anthropic
    - logging
    - dotenv
"""

import anthropic
import logging
import os
from dotenv import load_dotenv
from typing import Optional

DEFAULT_MODEL_NAME = "claude-3-7"

class ClaudeClient:
    def __init__(self):
        """
        Initializes the Claude client.
        """
        self.logger = logging.getLogger(__name__)  # Create a logger for this class
        self.logger.info("Initializing ClaudeClient.")
        load_dotenv()  # Load environment variables from .env file
        self.api_key: str = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            self.logger.error("API key not found in .env file.")
            raise ValueError("API key must be provided in the .env file.")
        self.client = anthropic.Anthropic(api_key=self.api_key)

    def generate_text(self, prompt: str, model_name: str = DEFAULT_MODEL_NAME, max_tokens: int = 1024) -> str:
        """
        Generates text based on a prompt using the specified model.
        
        Args:
            prompt (str): Input text for generation.
            model_name (str): Name of the model to use (default: DEFAULT_MODEL_NAME).
            max_tokens (int): Maximum number of tokens to generate (default: 1024).
        
        Returns:
            str: Generated response as text.

        Raises:
            ValueError: If the prompt is empty or invalid.
            RuntimeError: If text generation fails.
        """
        if not prompt.strip():
            self.logger.error("Prompt is empty or whitespace.")
            raise ValueError("Prompt cannot be empty or whitespace.")
        
        self.logger.info("Generating text using model '%s'.", model_name)
        try:
            response = self.client.messages.create(
                model=model_name,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}]
            )
            if not response or not response.get("completion"):
                self.logger.error("Received empty response from the model.")
                raise RuntimeError("Received empty response from the model.")
            self.logger.info("Text generation successful.")
            return response["completion"]
        except Exception as e:
            self.logger.error("Error during text generation: %s", e)
            raise RuntimeError("An unexpected error occurred during text generation.") from e