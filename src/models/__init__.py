"""
Module: models

This module consolidates all the models used in the application, providing
a unified interface for importing them.

Example:
    >>> from src.models import Message, RawResponse
"""

from .message import Message
from .raw_response import RawResponse

__all__ = ["Message", "RawResponse"]
