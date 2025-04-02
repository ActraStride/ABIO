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

DEFAULT_MODEL_NAME = "gemini-1.5-flash"

class GeminiClient:
    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initializes the Gemini client with the provided logger.
        
        Args:
            logger (Optional[logging.Logger]): Logger instance to use. Defaults to None.
        """
        load_dotenv()  # Load environment variables from .env file
        self.api_key: str = os.getenv("GEMINI_API_KEY")  # Ensure type is explicitly defined
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

    
    def count_tokens(self, text: str, model_name: str = DEFAULT_MODEL_NAME) -> int:
        """
        Counts the number of tokens in the given text using the specified model.

        Args:
            text (str): The text to count tokens for.
            model_name (str): Name of the model to use for token counting (default: DEFAULT_MODEL_NAME).

        Returns:
            int: The total number of tokens in the text.

        Raises:
            ValueError: If the text is empty or invalid.
            RuntimeError: If token counting fails.
        """
        if not text.strip():
            raise ValueError("Text cannot be empty or whitespace.")
        
        self.logger.info("Counting tokens for text using model '%s'.", model_name)
        try:
            model = genai.GenerativeModel(model_name)
            response = model.count_tokens(text)  # Assuming this returns an object
            total_tokens = response.total_tokens  # Extract the integer value
            self.logger.info("Token count successful. Total tokens: %d", total_tokens)
            return total_tokens
        except AttributeError:
            self.logger.error("Unexpected response format from count_tokens.")
            raise RuntimeError("Failed to count tokens due to unexpected response format.")
        except Exception as e:
            self.logger.error("Error counting tokens: %s", e)
            raise RuntimeError("Failed to count tokens.") from e

    def generate_text(self, prompt: str, model_name: str = DEFAULT_MODEL_NAME) -> str:
        """
        Generates text based on a prompt using the specified model and logs token counts.
        
        Args:
            prompt (str): Input text for generation.
            model_name (str): Name of the model to use (default: DEFAULT_MODEL_NAME).
        
        Returns:
            str: Generated response as text.

        Raises:
            ValueError: If the prompt is empty or invalid.
            RuntimeError: If text generation fails.
        """
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty or whitespace.")
        
        self.logger.info("Generating text using model '%s'.", model_name)
        try:
            # Count tokens in the prompt
            prompt_tokens = self.count_tokens(prompt, model_name)
            self.logger.info("Prompt token count: %d", prompt_tokens)

            # Generate text
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            if not response or not response.text:
                raise RuntimeError("Received empty response from the model.")
            
            # Count tokens in the response
            response_tokens = self.count_tokens(response.text, model_name)
            self.logger.info("Response token count: %d", response_tokens)

            self.logger.info("Text generation successful.")
            return response.text
        except genai.exceptions.ModelNotFoundError as e:
            self.logger.error("Model '%s' not found: %s", model_name, e)
            raise RuntimeError(f"Model '{model_name}' not found.") from e
        except genai.exceptions.GenerationError as e:
            self.logger.error("Error during text generation: %s", e)
            raise RuntimeError("Text generation failed due to an SDK error.") from e
        except Exception as e:
            self.logger.error("Unexpected error during text generation: %s", e)
            raise RuntimeError("An unexpected error occurred during text generation.") from e

    def is_model_supported(self, model_name: str) -> bool:
        """
        Checks if a model is supported for content generation.
        
        Args:
            model_name (str): Name of the model to check.
        
        Returns:
            bool: True if the model is supported, False otherwise.
        """
        try:
            return model_name in self.list_models()
        except RuntimeError:
            self.logger.warning("Could not validate model '%s'.", model_name)
            return False