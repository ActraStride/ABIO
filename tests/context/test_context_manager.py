"""
Module Name: test_context_manager

Unit tests for the ContextManager class from the context_manager module.

This module provides comprehensive test coverage for the ContextManager class,
including initialization scenarios, message management, context window limitations,
and error handling. All tests focus on verifying the functionality of the
context management system without external dependencies.

Example:
    Run these tests using pytest or unittest:
    >>> python -m unittest tests.context.test_context_manager
    >>> pytest tests/context/test_context_manager.py

Dependencies:
    - unittest
    - unittest.mock
    - logging
    - typing
    - src.context.context_manager
    - src.models.message
"""

import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import logging
from typing import List, Optional

# Add the project root to Python path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.context.context_manager import ContextManager
from src.models.message import Message


class TestContextManager(unittest.TestCase):
    """
    Test suite for the ContextManager class.
    
    This class contains unit tests that verify the proper initialization,
    message management, context window limitations, and error handling
    of the ContextManager.
    """
    
    def setUp(self) -> None:
        """
        Set up the test environment before each test case.
        
        This method disables logging during tests to keep test output clean
        and initializes any common test objects.
        """
        # Disable logging for cleaner test output
        logging.disable(logging.CRITICAL)
        
    def tearDown(self) -> None:
        """
        Clean up the test environment after each test case.
        
        This method re-enables logging after tests.
        """
        # Re-enable logging for other tests
        logging.disable(logging.NOTSET)
        
    def test_init_default(self) -> None:
        """
        Test default initialization of ContextManager.
        
        Verifies that the ContextManager initializes with empty messages
        and no message limit when no parameters are provided.
        
        Raises:
            AssertionError: If the initialized state doesn't match expectations.
        """
        # Initialize with default parameters
        context = ContextManager()
        
        # Verify initial state
        self.assertEqual([], context.messages)
        self.assertIsNone(context.message_limit)
        
    def test_init_with_message_limit(self) -> None:
        """
        Test initialization with a message limit.
        
        Verifies that the ContextManager correctly sets the message limit
        when provided during initialization.
        
        Raises:
            AssertionError: If the message limit isn't set correctly.
        """
        # Initialize with a specific message limit
        message_limit = 10
        context = ContextManager(message_limit=message_limit)
        
        # Verify message limit is set
        self.assertEqual(message_limit, context.message_limit)
        self.assertEqual([], context.messages)
        
    def test_init_with_context_messages(self) -> None:
        """
        Test initialization with preexisting context messages.
        
        Verifies that the ContextManager correctly initializes with
        provided context messages.
        
        Raises:
            AssertionError: If the initial messages aren't set correctly.
        """
        # Create some initial messages
        initial_messages = [
            Message(role="system", content="System message"),
            Message(role="user", content="User message")
        ]
        
        # Initialize with context messages
        context = ContextManager(context_messages=initial_messages)
        
        # Verify messages are set
        self.assertEqual(initial_messages, context.messages)
        self.assertIsNone(context.message_limit)
        
    def test_add_message(self) -> None:
        """
        Test adding a valid message to the context.
        
        Verifies that a message is correctly added to the context
        and appears in the message list.
        
        Raises:
            AssertionError: If the message isn't added correctly.
        """
        # Initialize context manager
        context = ContextManager()
        
        # Create and add a message
        message = Message(role="user", content="Hello, world!")
        context.add_message(message)
        
        # Verify message was added
        self.assertEqual(1, len(context.messages))
        self.assertEqual(message, context.messages[0])
        
    def test_add_message_empty_role(self) -> None:
        """
        Test adding a message with an empty role.
        
        Verifies that attempting to add a message with an empty role
        raises a ValueError with an appropriate message.
        
        Raises:
            AssertionError: If the expected exception is not raised or
                           if the error message doesn't match expectations.
        """
        # Initialize context manager
        context = ContextManager()
        
        # Attempt to add a message with empty role
        with self.assertRaises(ValueError) as context_ex:
            context.add_message(Message(role="", content="Content"))
            
        # Verify exception message
        self.assertEqual("Role cannot be empty or whitespace.", str(context_ex.exception))
        
        # Verify no message was added
        self.assertEqual(0, len(context.messages))
        
    def test_add_message_whitespace_role(self) -> None:
        """
        Test adding a message with a whitespace-only role.
        
        Verifies that attempting to add a message with a role containing
        only whitespace raises a ValueError with an appropriate message.
        
        Raises:
            AssertionError: If the expected exception is not raised or
                           if the error message doesn't match expectations.
        """
        # Initialize context manager
        context = ContextManager()
        
        # Attempt to add a message with whitespace role
        with self.assertRaises(ValueError) as context_ex:
            context.add_message(Message(role="   ", content="Content"))
            
        # Verify exception message
        self.assertEqual("Role cannot be empty or whitespace.", str(context_ex.exception))
        
        # Verify no message was added
        self.assertEqual(0, len(context.messages))
        
    def test_add_message_empty_content(self) -> None:
        """
        Test adding a message with an empty content.
        
        Verifies that attempting to add a message with empty content
        raises a ValueError with an appropriate message.
        
        Raises:
            AssertionError: If the expected exception is not raised or
                           if the error message doesn't match expectations.
        """
        # Initialize context manager
        context = ContextManager()
        
        # Attempt to add a message with empty content
        with self.assertRaises(ValueError) as context_ex:
            context.add_message(Message(role="user", content=""))
            
        # Verify exception message
        self.assertEqual("Content cannot be empty or whitespace.", str(context_ex.exception))
        
        # Verify no message was added
        self.assertEqual(0, len(context.messages))
        
    def test_add_message_whitespace_content(self) -> None:
        """
        Test adding a message with whitespace-only content.
        
        Verifies that attempting to add a message with content containing
        only whitespace raises a ValueError with an appropriate message.
        
        Raises:
            AssertionError: If the expected exception is not raised or
                           if the error message doesn't match expectations.
        """
        # Initialize context manager
        context = ContextManager()
        
        # Attempt to add a message with whitespace content
        with self.assertRaises(ValueError) as context_ex:
            context.add_message(Message(role="user", content="  \n  "))
            
        # Verify exception message
        self.assertEqual("Content cannot be empty or whitespace.", str(context_ex.exception))
        
        # Verify no message was added
        self.assertEqual(0, len(context.messages))
        
    def test_add_multiple_messages(self) -> None:
        """
        Test adding multiple messages to the context.
        
        Verifies that multiple messages are correctly added to the context
        and appear in the message list in the correct order.
        
        Raises:
            AssertionError: If the messages aren't added correctly or
                           if the order isn't maintained.
        """
        # Initialize context manager
        context = ContextManager()
        
        # Create and add multiple messages
        messages = [
            Message(role="user", content="Hello"),
            Message(role="assistant", content="Hi there"),
            Message(role="user", content="How are you?")
        ]
        
        for msg in messages:
            context.add_message(msg)
            
        # Verify all messages were added in order
        self.assertEqual(3, len(context.messages))
        for i, msg in enumerate(messages):
            self.assertEqual(msg, context.messages[i])
            
    def test_get_recent_messages_all(self) -> None:
        """
        Test retrieving all messages when there are fewer than requested.
        
        Verifies that get_recent_messages returns all messages when there
        are fewer messages than the number requested.
        
        Raises:
            AssertionError: If the wrong messages are returned.
        """
        # Initialize context manager with messages
        messages = [
            Message(role="user", content="Hello"),
            Message(role="assistant", content="Hi there")
        ]
        context = ContextManager(context_messages=messages)
        
        # Get recent messages (more than exist)
        recent = context.get_recent_messages(n=5)
        
        # Verify all messages are returned
        self.assertEqual(messages, recent)
        
    def test_get_recent_messages_partial(self) -> None:
        """
        Test retrieving a subset of recent messages.
        
        Verifies that get_recent_messages returns the correct number of
        most recent messages when there are more messages than requested.
        
        Raises:
            AssertionError: If the wrong messages are returned.
        """
        # Initialize context manager with messages
        messages = [
            Message(role="system", content="System init"),
            Message(role="user", content="Hello"),
            Message(role="assistant", content="Hi there"),
            Message(role="user", content="How are you?"),
            Message(role="assistant", content="I'm good!")
        ]
        context = ContextManager(context_messages=messages)
        
        # Get recent messages (fewer than exist)
        recent = context.get_recent_messages(n=3)
        
        # Verify only the most recent messages are returned
        self.assertEqual(messages[-3:], recent)
        
    def test_get_recent_messages_invalid_n(self) -> None:
        """
        Test retrieving messages with an invalid count parameter.
        
        Verifies that get_recent_messages raises a ValueError when
        called with n <= 0.
        
        Raises:
            AssertionError: If the expected exception is not raised or
                           if the error message doesn't match expectations.
        """
        # Initialize context manager
        context = ContextManager()
        
        # Try to get messages with invalid n
        with self.assertRaises(ValueError) as context_ex:
            context.get_recent_messages(n=0)
            
        # Verify exception message
        self.assertEqual("The number of messages to retrieve must be greater than 0.", 
                         str(context_ex.exception))
                         
        # Try with negative n
        with self.assertRaises(ValueError):
            context.get_recent_messages(n=-5)
            
    def test_clear_context(self) -> None:
        """
        Test clearing the conversation context.
        
        Verifies that clear_context removes all messages from the context.
        
        Raises:
            AssertionError: If messages remain after clearing.
        """
        # Initialize context manager with messages
        messages = [
            Message(role="user", content="Hello"),
            Message(role="assistant", content="Hi there")
        ]
        context = ContextManager(context_messages=messages)
        
        # Verify initial state
        self.assertEqual(2, len(context.messages))
        
        # Clear context
        context.clear_context()
        
        # Verify all messages were removed
        self.assertEqual(0, len(context.messages))
        
    def test_trim_messages_no_limit(self) -> None:
        """
        Test message trimming with no message limit.
        
        Verifies that _trim_messages doesn't remove any messages when
        no message limit is set.
        
        Raises:
            AssertionError: If any messages are removed when they shouldn't be.
        """
        # Initialize context manager with messages but no limit
        messages = [
            Message(role="user", content="Hello"),
            Message(role="assistant", content="Hi there")
        ]
        context = ContextManager(context_messages=messages)
        
        # Call trim_messages (should do nothing)
        context._trim_messages()
        
        # Verify no messages were removed
        self.assertEqual(2, len(context.messages))
        self.assertEqual(messages, context.messages)
        
    def test_trim_messages_under_limit(self) -> None:
        """
        Test message trimming when under the message limit.
        
        Verifies that _trim_messages doesn't remove any messages when
        the number of messages is less than the limit.
        
        Raises:
            AssertionError: If any messages are removed when they shouldn't be.
        """
        # Initialize context manager with messages and a higher limit
        messages = [
            Message(role="user", content="Hello"),
            Message(role="assistant", content="Hi there")
        ]
        context = ContextManager(message_limit=5, context_messages=messages)
        
        # Call trim_messages (should do nothing)
        context._trim_messages()
        
        # Verify no messages were removed
        self.assertEqual(2, len(context.messages))
        self.assertEqual(messages, context.messages)
        
    def test_trim_messages_at_limit(self) -> None:
        """
        Test message trimming when at the message limit.
        
        Verifies that _trim_messages doesn't remove any messages when
        the number of messages equals the limit.
        
        Raises:
            AssertionError: If any messages are removed when they shouldn't be.
        """
        # Initialize context manager with messages and an equal limit
        messages = [
            Message(role="user", content="Hello"),
            Message(role="assistant", content="Hi there")
        ]
        context = ContextManager(message_limit=2, context_messages=messages)
        
        # Call trim_messages (should do nothing)
        context._trim_messages()
        
        # Verify no messages were removed
        self.assertEqual(2, len(context.messages))
        self.assertEqual(messages, context.messages)
        
    def test_trim_messages_over_limit(self) -> None:
        """
        Test message trimming when over the message limit.
        
        Verifies that _trim_messages removes the oldest messages to
        bring the count down to the limit.
        
        Raises:
            AssertionError: If the wrong messages are removed or if
                           the count doesn't match the limit after trimming.
        """
        # Initialize context manager with messages and a lower limit
        messages = [
            Message(role="system", content="System init"),
            Message(role="user", content="Hello"),
            Message(role="assistant", content="Hi there"),
            Message(role="user", content="How are you?"),
            Message(role="assistant", content="I'm good!")
        ]
        limit = 3
        context = ContextManager(message_limit=limit, context_messages=messages)
        
        # Call trim_messages
        context._trim_messages()
        
        # Verify oldest messages were removed
        self.assertEqual(limit, len(context.messages))
        self.assertEqual(messages[-limit:], context.messages)
        
    def test_add_message_triggers_trim(self) -> None:
        """
        Test that adding a message triggers trimming.
        
        Verifies that add_message calls _trim_messages to ensure
        the message limit is maintained.
        
        Raises:
            AssertionError: If trimming doesn't occur after adding a message.
        """
        # Initialize context manager with messages at the limit
        messages = [
            Message(role="user", content="Hello"),
            Message(role="assistant", content="Hi there")
        ]
        limit = 2
        context = ContextManager(message_limit=limit, context_messages=messages)
        
        # Mock _trim_messages to track calls
        original_trim = context._trim_messages
        context._trim_messages = MagicMock(wraps=original_trim)
        
        # Add a new message (should trigger trim)
        new_message = Message(role="user", content="New message")
        context.add_message(new_message)
        
        # Verify _trim_messages was called
        context._trim_messages.assert_called_once()
        
        # Verify we still have 'limit' messages (oldest was removed)
        self.assertEqual(limit, len(context.messages))
        self.assertEqual([messages[1], new_message], context.messages)
        
    def test_close_method(self) -> None:
        """
        Test the close method for cleanup.
        
        Verifies that the close method executes without errors and
        performs any necessary cleanup.
        
        Raises:
            AssertionError: If the close method raises an exception.
        """
        # Initialize context manager
        context = ContextManager()
        
        # Verify close can be called without errors
        try:
            context.close()
        except Exception as e:
            self.fail(f"close() raised {type(e).__name__} unexpectedly: {e}")
            
    def test_close_method_handles_exceptions(self) -> None:
        """
        Test exception handling in the close method.
        
        Verifies that the close method properly handles exceptions that
        might occur during cleanup.
        
        Raises:
            AssertionError: If exceptions aren't properly handled.
        """
        # Initialize context manager
        context = ContextManager()
        
        # Mock the logger to verify error logging
        mock_logger = MagicMock()
        context.logger = mock_logger
        
        # Create a scenario where an exception occurs during close
        with patch.object(context.logger, 'info', side_effect=Exception("Test error")):
            # Verify close handles the exception without re-raising
            try:
                context.close()
            except Exception as e:
                self.fail(f"close() didn't handle exception: {e}")
                
        # Verify the error was logged
        mock_logger.error.assert_called_once()
        # Check that the error message contains our exception text
        self.assertIn("Test error", mock_logger.error.call_args[0][1])


if __name__ == '__main__':
    unittest.main()