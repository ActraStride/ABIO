"""
Module Name: test_gemini_client

Unit tests for the GeminiClient class from the gemini_client module.

This module provides comprehensive test coverage for the GeminiClient class,
including initialization scenarios, API configuration, and error handling.
All tests use mock objects to avoid actual API calls during testing.

Example:
    Run these tests using pytest or unittest:
    >>> python -m unittest tests.clients.test_gemini_client
    >>> pytest tests/clients/test_gemini_client.py

Dependencies:
    - unittest
    - unittest.mock
    - os
    - sys
    - logging
"""

import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import logging
from typing import Optional

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.clients.gemini_client import GeminiClient

TEST_API_KEY = "test_api_key_from_setup"

class TestGeminiClient(unittest.TestCase):
    """
    Test suite for the GeminiClient class.
    
    This class contains unit tests that verify the proper initialization,
    configuration, and error handling of the GeminiClient. It uses mock objects
    to isolate tests from external dependencies.
    """

    load_dotenv_patcher: Optional[any] = None
    genai_patcher: Optional[any] = None
    env_patcher: Optional[any] = None
    mock_load_dotenv: Optional[MagicMock] = None
    mock_genai: Optional[MagicMock] = None

    def setUp(self) -> None:
        """
        Set up the test environment before each test case.
        
        This method:
        - Patches the load_dotenv function to prevent actual .env file loading
        - Patches the genai module to prevent actual API calls
        - Sets a mock environment variable for the API key
        - Disables logging during tests to keep test output clean
        """
        self.load_dotenv_patcher = patch('src.clients.gemini_client.load_dotenv', return_value=False)
        self.mock_load_dotenv = self.load_dotenv_patcher.start()

        self.genai_patcher = patch('src.clients.gemini_client.genai')
        self.mock_genai = self.genai_patcher.start()

        self.env_patcher = patch.dict(os.environ, {"GEMINI_API_KEY": TEST_API_KEY}, clear=True)
        self.env_patcher.start()

        logging.disable(logging.CRITICAL)

    def tearDown(self) -> None:
        """
        Clean up the test environment after each test case.
        
        This method:
        - Stops all patch objects to restore original functionality
        - Re-enables logging for other tests
        """
        self.env_patcher.stop()
        self.genai_patcher.stop()
        self.load_dotenv_patcher.stop()

        logging.disable(logging.NOTSET)

    def test_init_missing_api_key(self) -> None:
        """
        Test initialization with a missing API key.
        
        Verifies that the client raises a ValueError with an appropriate
        message when initialized without an API key in the environment.
        
        Raises:
            AssertionError: If the expected exception is not raised or
                           if the error message doesn't match expectations.
        """
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError) as context:
                client = GeminiClient()

            self.assertIn("API key must be provided", str(context.exception))

        self.mock_load_dotenv.assert_called_once()

    def test_configure_api_success(self) -> None:
        """
        Test successful API configuration.
        
        Verifies that the client correctly configures the Gemini SDK
        with the API key from the environment when initialized successfully.
        
        Raises:
            AssertionError: If the SDK is not configured with the correct API key
                           or if load_dotenv is not called.
        """
        client = GeminiClient()

        self.mock_genai.configure.assert_called_once_with(api_key=TEST_API_KEY)
        self.mock_load_dotenv.assert_called_once()

if __name__ == '__main__':
    unittest.main()