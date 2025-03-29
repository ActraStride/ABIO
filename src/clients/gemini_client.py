"""
Module Name: gemini_client

Client for interacting with the Gemini generative AI service.

This module provides a wrapper around the Gemini SDK, enabling:
- Configuration of the Gemini API with an API key.
- Retrieval of available models for content generation.
- Text generation using a specified model.

Example:
    >>> from src.clients.gemini_client import GeminiClient
    >>> client = GeminiClient(api_key="your_api_key")
    >>> models = client.list_models()
    >>> print(models)
    >>> response = client.generate_text(prompt="Hello, world!")
    >>> print(response)

Dependencies:
    - google.generativeai
    - logging
    - IPython.display
"""

import google.generativeai as genai
import textwrap
import logging
import os
from dotenv import load_dotenv
from typing import List, Optional
from IPython.display import Markdown

class GeminiClient:
    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initializes the Gemini client with the provided logger.
        
        Args:
            logger (Optional[logging.Logger]): Logger instance to use. Defaults to None.
        """
        load_dotenv()  # Load environment variables from .env file
        self.api_key: str = os.getenv("API_KEY")  # Ensure type is explicitly defined
        if not self.api_key:
            raise ValueError("API key must be provided in the .env file.")
        self.logger: logging.Logger = logger or logging.getLogger(__name__)
        self.logger.info("Initializing GeminiClient with API key from .env.")
        self._configure_api()

    def _configure_api(self) -> None:
        """
        Configures the Gemini SDK with the API key.

        Raises:
            RuntimeError: If the SDK configuration fails.
        """
        try:
            genai.configure(api_key=self.api_key)
            self.logger.info("Gemini SDK configured successfully.")
        except Exception as e:
            self.logger.error("Failed to configure Gemini SDK: %s", e)
            raise RuntimeError("Gemini SDK configuration failed.") from e

    def list_models(self) -> List[str]:
        """
        Lists the available models that support content generation.
        
        Returns:
            List[str]: List of compatible model names.

        Raises:
            RuntimeError: If fetching models fails.
        """
        self.logger.info("Fetching list of available models.")
        try:
            models = [
                model.name
                for model in genai.list_models()
                if 'generateContent' in model.supported_generation_methods
            ]
            self.logger.info("Successfully retrieved %d models.", len(models))
            return models
        except Exception as e:
            self.logger.error("Error fetching models: %s", e)
            raise RuntimeError("Failed to fetch models.") from e

    def generate_text(self, prompt: str, model_name: str = "gemini-1.5-flash") -> str:
        """
        Generates text based on a prompt using the specified model.
        
        Args:
            prompt (str): Input text for generation.
            model_name (str): Name of the model to use (default: gemini-1.5-flash).
        
        Returns:
            str: Generated response as text.

        Raises:
            RuntimeError: If text generation fails.
        """
        self.logger.info("Generating text using model '%s'.", model_name)
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            self.logger.info("Text generation successful.")
            return response.text
        except Exception as e:
            self.logger.error("Error generating text: %s", e)
            raise RuntimeError("Text generation failed.") from e