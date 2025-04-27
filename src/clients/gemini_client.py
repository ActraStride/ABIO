"""
Module Name: gemini_client

Client for interacting with the Gemini generative AI service.

This module provides a wrapper around the Gemini SDK, enabling:
- Configuration of the Gemini API with an API key.
- Retrieval of available models for content generation.
- Text generation using a specified model.
- Token counting for input and generated text.

Example:
    >>> from src.clients.gemini_client import GeminiClient
    >>> client = GeminiClient(api_key="your_api_key")
    >>> models = client.list_models()
    >>> print(models)
    >>> response = client.generate_text(prompt="Hello, world!")
    >>> print(response.generated_text)

Dependencies:
    - google.generativeai
    - logging
    - IPython.display
    - python-dotenv
"""

import google.generativeai as genai
import textwrap
import logging
import os
from dotenv import load_dotenv
from typing import List, Optional, Dict, Any
from IPython.display import Markdown

from src.models.raw_response import RawResponse

DEFAULT_MODEL_NAME = "gemini-1.5-flash"

class GeminiClient:
    def __init__(self, model_name: str = DEFAULT_MODEL_NAME) -> None:
        """
        Initializes the Gemini client by loading the API key from the environment
        and configuring the Gemini SDK.

        Raises:
            ValueError: If the API key is not found in the environment variables.
        """
        self.model_name: str = model_name
        self.logger = logging.getLogger(__name__)  # Create a logger for this class
        self.logger.info("Initializing GeminiClient.")
        load_dotenv()  # Load environment variables from .env file
        self.api_key: str = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            self.logger.error("API key not found in .env file.")
            raise ValueError("API key must be provided in the .env file.")
        self._grpc_channel = None  # Placeholder for gRPC channel (if applicable)
        self._configure_api()

    def _configure_api(self) -> None:
        """
        Configures the Gemini SDK with the API key.

        Raises:
            RuntimeError: If the SDK configuration fails due to an error.
        """
        try:
            genai.configure(api_key=self.api_key)
            self.logger.info("Gemini SDK configured successfully.")
        except Exception as e:
            self.logger.error("Failed to configure Gemini SDK: %s", e)
            raise RuntimeError("Gemini SDK configuration failed.") from e

    def list_models(self) -> List[str]:
        """
        Retrieves a list of available models that support content generation.

        Returns:
            List[str]: A list of model names that can generate content.

        Raises:
            RuntimeError: If there is an error while fetching the models.
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

    
    def count_tokens(self, text: str) -> int:
        """
        Counts the number of tokens in the provided text using the specified model.

        Args:
            text (str): The input text for which tokens need to be counted.

        Returns:
            int: The total number of tokens in the input text.

        Raises:
            ValueError: If the input text is empty or invalid.
            RuntimeError: If there is an error during token counting.
        """
        if not text.strip():
            raise ValueError("Text cannot be empty or whitespace.")
        
        self.logger.info("Counting tokens for text using model '%s'.", self.model_name)
        try:
            model = genai.GenerativeModel(self.model_name)
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

    def generate_text(self, prompt: str) -> RawResponse:
        """
        Generates text based on the provided prompt using the specified model.

        Args:
            prompt (str): The input text to generate content from.

        Returns:
            RawResponse: An object containing the generated text, token counts, 
                         model name, and additional metadata.

        Raises:
            ValueError: If the prompt is empty or invalid.
            RuntimeError: If text generation fails due to an SDK or unexpected error.
        """
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty or whitespace.")
        
        self.logger.info("Generating text using model '%s'.", self.model_name)
        try:
            # Count tokens in the prompt
            prompt_tokens = self.count_tokens(prompt)
            self.logger.info("Prompt token count: %d", prompt_tokens)

            # Generate text
            model = genai.GenerativeModel(self.model_name)
            response = model.generate_content(prompt)
            self.logger.info("Text generation response: %s", response)
            if not response or not response.text:
                raise RuntimeError("Received empty response from the model.")
            
            # Count tokens in the response
            response_tokens = self.count_tokens(response.text)
            self.logger.info("Response token count: %d", response_tokens)

            self.logger.info("Text generation successful.")

            # Return a detailed response
            return RawResponse(
                generated_text=response.text,
                prompt_tokens=prompt_tokens,
                response_tokens=response_tokens,
                model_name=self.model_name,
                metadata=response.metadata if hasattr(response, "metadata") else None
            )
        
        except genai.exceptions.ModelNotFoundError as e:
            self.logger.error("Model '%s' not found: %s", self.model_name, e)
            raise RuntimeError(f"Model '{self.model_name}' not found.") from e
        except genai.exceptions.GenerationError as e:
            self.logger.error("Error during text generation: %s", e)
            raise RuntimeError("Text generation failed due to an SDK error.") from e
        except Exception as e:
            self.logger.error("Unexpected error during text generation: %s", e)
            raise RuntimeError("An unexpected error occurred during text generation.") from e

    def is_model_supported(self) -> bool:
        """
        Checks if the specified model is supported for content generation.

        Returns:
            bool: True if the model is supported, False otherwise.
        """
        try:
            return self.model_name in self.list_models()
        except RuntimeError:
            self.logger.warning("Could not validate model '%s'.", self.model_name)
            return False

    def close(self) -> None:
        """
        Performs cleanup for the Gemini SDK, if applicable.

        This method is a placeholder for any SDK-specific cleanup logic that 
        might be required in the future.
        """
        try:
            self.logger.info("Performing cleanup for Gemini SDK.")
            # Add any SDK-specific cleanup logic here if needed in the future.
        except Exception as e:
            self.logger.error("Error during SDK cleanup: %s", e)