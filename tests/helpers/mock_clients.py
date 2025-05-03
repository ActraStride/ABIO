"""
Module: mock_clients

Helper module for creating mock clients for testing.

This module provides factory functions for creating consistently configured
mock objects of various API clients used in the ABIO system. It also injects 
mock exception classes into the mocked SDK (e.g., genai.exceptions)
to support error-handling tests without relying on the real SDK.

Example:
    >>> from tests.helpers.mock_clients import setup_gemini_mocks, teardown_gemini_mocks
    >>> 
    >>> # Create mocks for testing
    >>> mocks = setup_gemini_mocks()
    >>> 
    >>> # Run tests with mocked dependencies
    >>> from src.clients.gemini_client import GeminiClient
    >>> client = GeminiClient()
    >>> 
    >>> # Make assertions using mocks
    >>> assert mocks["mocks"]["genai"].GenerativeModel.called
    >>> 
    >>> # Clean up after tests
    >>> teardown_gemini_mocks(mocks)

Dependencies:
    - unittest.mock (patch, MagicMock)
    - os
    - types
    - typing
"""

from unittest.mock import patch, MagicMock
import os
import types
from typing import Dict, Any

DEFAULT_TEST_API_KEY = "test_api_key"

def setup_gemini_mocks(api_key: str = DEFAULT_TEST_API_KEY) -> Dict[str, Any]:
    """
    Setup all mocks required for testing the GeminiClient.

    This includes:
    - Patching environment variables with a test API key.
    - Patching 'load_dotenv' to prevent loading real environment files.
    - Patching the 'genai' module used inside the GeminiClient.
    - Injecting dummy exception classes into genai.exceptions.

    Args:
        api_key: Optional custom API key to use in the mock.

    Returns:
        Dict containing:
            - "patchers": All patch objects that need to be stopped in teardown.
            - "mocks": Mock objects for assertions and test usage.
    """
    # Create patchers
    load_dotenv_patcher = patch('src.clients.gemini_client.load_dotenv', return_value=False)
    genai_patcher = patch('src.clients.gemini_client.genai')
    env_patcher = patch.dict(os.environ, {"GEMINI_API_KEY": api_key}, clear=True)

    # Start patchers
    mock_load_dotenv = load_dotenv_patcher.start()
    mock_genai = genai_patcher.start()
    env_patcher.start()

    # Inject mock exception classes into the mocked genai module
    mock_genai.exceptions = types.SimpleNamespace(
        ModelNotFoundError=type("ModelNotFoundError", (Exception,), {}),
        GenerationError=type("GenerationError", (Exception,), {})
    )

    return {
        "patchers": {
            "load_dotenv": load_dotenv_patcher,
            "genai": genai_patcher,
            "env": env_patcher
        },
        "mocks": {
            "load_dotenv": mock_load_dotenv,
            "genai": mock_genai
        }
    }

def teardown_gemini_mocks(mocks_dict: Dict[str, Any]) -> None:
    """
    Stop all patchers created by setup_gemini_mocks.

    This ensures a clean state between tests and prevents memory leaks or
    unexpected behavior due to lingering mocks.

    Args:
        mocks_dict: The dictionary returned by setup_gemini_mocks.
    """
    for patcher in mocks_dict["patchers"].values():
        patcher.stop()
