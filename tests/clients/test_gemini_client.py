"""
Test module for the GeminiClient class.

This module contains unit tests for testing the functionality of the GeminiClient
class which interacts with the Gemini generative AI service.
"""

import unittest
from unittest.mock import patch, MagicMock, PropertyMock
import os
import sys
import logging
from typing import List, Dict, Any

# Add the root directory to the path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.clients.gemini_client import GeminiClient
from src.models.raw_response import RawResponse

class TestGeminiClient(unittest.TestCase):
    """Test cases for the GeminiClient class."""

    @patch.dict(os.environ, {"GEMINI_API_KEY": "test_api_key"})
    @patch('src.clients.gemini_client.genai')
    def setUp(self, mock_genai):
        """Set up test fixtures before executing each test method."""
        self.mock_genai = mock_genai
        # Configure the mock to avoid actual API calls
        self.client = GeminiClient()
        # Disable logging during tests
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        """Clean up after each test method has run."""
        # Re-enable logging
        logging.disable(logging.NOTSET)

    @patch.dict(os.environ, {})
    def test_init_missing_api_key(self):
        """Test initialization failure when API key is missing."""
        with self.assertRaises(ValueError):
            client = GeminiClient()

    # @patch('src.clients.gemini_client.genai')
    # def test_configure_api_success(self, mock_genai):
    #     """Test successful API configuration."""
    #     # Already tested in setUp, but we can test it explicitly
    #     client = GeminiClient()
    #     mock_genai.configure.assert_called_once_with(api_key="test_api_key")

    # @patch('src.clients.gemini_client.genai')
    # def test_configure_api_failure(self, mock_genai):
    #     """Test API configuration failure."""
    #     mock_genai.configure.side_effect = Exception("API configuration failed")
    #     with self.assertRaises(RuntimeError):
    #         client = GeminiClient()

    # def test_list_models_success(self):
    #     """Test successful model listing."""
    #     # Create a mock model
    #     mock_model1 = MagicMock()
    #     mock_model1.name = "gemini-1.5-flash"
    #     mock_model1.supported_generation_methods = ['generateContent']
        
    #     mock_model2 = MagicMock()
    #     mock_model2.name = "gemini-1.0-pro"
    #     mock_model2.supported_generation_methods = ['generateContent']
        
    #     # Configure the mock to return our mock models
    #     self.mock_genai.list_models.return_value = [mock_model1, mock_model2]
        
    #     # Call the method
    #     models = self.client.list_models()
        
    #     # Assertions
    #     self.assertEqual(len(models), 2)
    #     self.assertIn("gemini-1.5-flash", models)
    #     self.assertIn("gemini-1.0-pro", models)
    #     self.mock_genai.list_models.assert_called_once()

    # def test_list_models_failure(self):
    #     """Test model listing failure."""
    #     self.mock_genai.list_models.side_effect = Exception("API error")
    #     with self.assertRaises(RuntimeError):
    #         self.client.list_models()

    # def test_count_tokens_empty_text(self):
    #     """Test token counting with empty text."""
    #     with self.assertRaises(ValueError):
    #         self.client.count_tokens("")

    # def test_count_tokens_success(self):
    #     """Test successful token counting."""
    #     # Configure the mock
    #     mock_model = MagicMock()
    #     self.mock_genai.GenerativeModel.return_value = mock_model
        
    #     # Create a mock response with a total_tokens property
    #     mock_response = MagicMock()
    #     mock_response.total_tokens = 10
    #     mock_model.count_tokens.return_value = mock_response
        
    #     # Call the method
    #     token_count = self.client.count_tokens("Hello, world!")
        
    #     # Assertions
    #     self.assertEqual(token_count, 10)
    #     self.mock_genai.GenerativeModel.assert_called_once_with("gemini-1.5-flash")
    #     mock_model.count_tokens.assert_called_once_with("Hello, world!")

    # def test_count_tokens_failure(self):
    #     """Test token counting failure."""
    #     mock_model = MagicMock()
    #     self.mock_genai.GenerativeModel.return_value = mock_model
    #     mock_model.count_tokens.side_effect = Exception("API error")
        
    #     with self.assertRaises(RuntimeError):
    #         self.client.count_tokens("Hello, world!")

    # def test_generate_text_empty_prompt(self):
    #     """Test text generation with empty prompt."""
    #     with self.assertRaises(ValueError):
    #         self.client.generate_text("")

    # def test_generate_text_success(self):
    #     """Test successful text generation."""
    #     # Mock the count_tokens method
    #     with patch.object(GeminiClient, 'count_tokens', return_value=5):
    #         # Configure the mock model
    #         mock_model = MagicMock()
    #         self.mock_genai.GenerativeModel.return_value = mock_model
            
    #         # Create a mock response
    #         mock_response = MagicMock()
    #         mock_response.text = "Generated text response"
    #         mock_model.generate_content.return_value = mock_response
            
    #         # Call the method
    #         response = self.client.generate_text("Hello, world!")
            
    #         # Assertions
    #         self.assertIsInstance(response, RawResponse)
    #         self.assertEqual(response.generated_text, "Generated text response")
    #         self.assertEqual(response.prompt_tokens, 5)
    #         self.assertEqual(response.response_tokens, 5)
    #         self.assertEqual(response.model_name, "gemini-1.5-flash")
            
    #         mock_model.generate_content.assert_called_once_with("Hello, world!")

    # def test_generate_text_model_not_found(self):
    #     """Test text generation with model not found error."""
    #     with patch.object(GeminiClient, 'count_tokens', return_value=5):
    #         mock_model = MagicMock()
    #         self.mock_genai.GenerativeModel.return_value = mock_model
            
    #         # Simulate a ModelNotFoundError
    #         self.mock_genai.exceptions.ModelNotFoundError = Exception
    #         mock_model.generate_content.side_effect = self.mock_genai.exceptions.ModelNotFoundError("Model not found")
            
    #         with self.assertRaises(RuntimeError):
    #             self.client.generate_text("Hello, world!")

    # def test_is_model_supported_true(self):
    #     """Test checking if a model is supported (true case)."""
    #     # Mock the list_models method to return a list including our model name
    #     with patch.object(GeminiClient, 'list_models', return_value=["gemini-1.5-flash", "gemini-1.0-pro"]):
    #         result = self.client.is_model_supported()
    #         self.assertTrue(result)

    # def test_is_model_supported_false(self):
    #     """Test checking if a model is supported (false case)."""
    #     # Mock the list_models method to return a list not including our model name
    #     with patch.object(GeminiClient, 'list_models', return_value=["other-model"]):
    #         result = self.client.is_model_supported()
    #         self.assertFalse(result)

    # def test_is_model_supported_error(self):
    #     """Test checking if a model is supported when list_models raises an error."""
    #     # Mock the list_models method to raise a RuntimeError
    #     with patch.object(GeminiClient, 'list_models', side_effect=RuntimeError("API error")):
    #         result = self.client.is_model_supported()
    #         self.assertFalse(result)

    # def test_close(self):
    #     """Test the close method."""
    #     # This is primarily a placeholder since close() doesn't do much yet
    #     self.client.close()
    #     # No assertion needed as we're just testing it runs without error

if __name__ == '__main__':
    unittest.main()