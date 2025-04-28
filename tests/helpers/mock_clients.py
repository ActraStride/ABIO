"""
Helper module for creating mock clients for testing.

This module provides factory functions for creating consistently configured
mock objects of various API clients used in the ABIO system.
"""

from unittest.mock import patch, MagicMock
import os
from typing import Tuple, Dict, Any

DEFAULT_TEST_API_KEY = "test_api_key"

def setup_gemini_mocks(api_key: str = DEFAULT_TEST_API_KEY) -> Dict[str, Any]:
    """
    Setup all mocks required for testing the GeminiClient.
    
    Args:
        api_key: Optional custom API key to use in the mock
        
    Returns:
        Dict containing all patchers and mocks:
        {
            "patchers": {...},  # All patch objects that need to be stopped
            "mocks": {...}      # Mock objects for assertions
        }
    """
    # Create patchers
    load_dotenv_patcher = patch('src.clients.gemini_client.load_dotenv', return_value=False)
    genai_patcher = patch('src.clients.gemini_client.genai')
    env_patcher = patch.dict(os.environ, {"GEMINI_API_KEY": api_key}, clear=True)
    
    # Start patchers
    mock_load_dotenv = load_dotenv_patcher.start()
    mock_genai = genai_patcher.start()
    env_patcher.start()
    
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
    
    Args:
        mocks_dict: The dictionary returned by setup_gemini_mocks
    """
    for patcher in mocks_dict["patchers"].values():
        patcher.stop()