"""
Module: abio_service

The core service layer for the ABIO chat system that orchestrates all functionality.

This module provides the ABIOService class which handles:
- Configuration management
- Model client initialization
- Chat session management
- Message processing
- Context handling

Example:
    >>> from src.services.abio_service import ABIOService
    >>> service = ABIOService(config_path="path/to/abiofile.yaml")
    >>> service.initialize()
    >>> session_id = service.create_session()
    >>> response = service.send_message(session_id, "Hello, how are you?")
    >>> print(response.content)
    >>> service.shutdown()

Dependencies:
    - logging
    - uuid
    - pathlib 
    - typing
    - src.clients.gemini_client
    - src.utils.setup_logging
    - src.chat.chat_session
    - src.config.agent_config
    - src.context.context_manager
    - src.embeddings.embeddings_generator
    - src.models.message
"""

import logging
import uuid
from pathlib import Path
from typing import Dict, List, Optional

from src.clients.gemini_client import GeminiClient
from src.utils.setup_logging import setup_logging
from src.chat.chat_session import ChatSession
from src.config.agent_config import ConfigManager
from src.context.context_manager import ContextManager
from src.embeddings.embeddings_generator import EmbeddingsGenerator
from src.models.message import Message


class ABIOService:
    """
    Service layer for ABIO chat system that encapsulates all core functionality.
    
    This class serves as the main entry point for applications interacting with the ABIO system.
    It manages configuration, model clients, chat sessions, and provides a high-level API.
    """
    
    def __init__(self, config_path: str = "Abiofile"):
        """
        Initialize the ABIO service.

        Args:
            config_path (str): Path to the ABIO configuration file.
            
        Raises:
            ValueError: If config_path is empty or None.
        """
        if not config_path or not config_path.strip():
            raise ValueError("config_path cannot be empty or None")
            
        self.config_path = config_path
        self.config_manager = None
        self.config = None
        self.clients: Dict[str, GeminiClient] = {}
        self.sessions: Dict[str, ChatSession] = {}
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing ABIOService with config path: %s", config_path)
        
    def initialize(self):
        """
        Initialize the service and required resources.
        
        This method sets up logging, loads configuration, and initializes 
        the default model client.
        
        Returns:
            ABIOService: Self reference for method chaining.
            
        Raises:
            RuntimeError: If initialization fails.
        """
        try:
            # Setup logging (consider making log path configurable)
            setup_logging(log_level="INFO", project_root=Path().absolute())
            
            # Load configuration
            self.config_manager = ConfigManager(config_path=self.config_path)
            self.config = self.config_manager.get_config()
            self.logger.info("Configuration loaded from %s", self.config_path)
            
            # Initialize default client
            self._initialize_default_client()
            return self
            
        except Exception as e:
            self.logger.error("Error initializing ABIOService: %s", e)
            raise RuntimeError(f"Failed to initialize ABIOService: {str(e)}") from e
        
    def _initialize_default_client(self):
        """
        Initialize the default model client.
        
        Raises:
            RuntimeError: If client initialization fails.
        """
        try:
            model_name = self.config.chat.default_model
            self.clients[model_name] = GeminiClient(model_name=model_name)
            self.logger.info("Initialized default model client: %s", model_name)
        except Exception as e:
            self.logger.error("Failed to initialize default client: %s", e)
            raise RuntimeError(f"Failed to initialize default client: {str(e)}") from e
        
    def create_session(self, user_id: Optional[str] = None) -> str:
        """
        Create a new chat session.

        Args:
            user_id (Optional[str]): Optional identifier for the user.

        Returns:
            str: The unique session ID.
            
        Raises:
            RuntimeError: If session creation fails.
        """
        try:
            session_id = str(uuid.uuid4())
            
            # Get the default client 
            model_name = self.config.chat.default_model
            if model_name not in self.clients:
                self.logger.error("Default model client not found: %s", model_name)
                raise ValueError(f"Default model client not initialized: {model_name}")
                
            client = self.clients[model_name]
            
            # Initialize session components
            message_limit = self.config.context.message_limit
            if message_limit is not None and message_limit <= 0:
                self.logger.warning("Invalid message limit: %s, using default", message_limit)
                message_limit = 10  # Default fallback
                
            context_manager = ContextManager(
                message_limit=message_limit,
                context_messages=self.config.context.context_messages
            )
            
            # Create chat session
            self.sessions[session_id] = ChatSession(
                session_id=session_id,
                client=client,
                context_manager=context_manager,
                embeddings_generator=EmbeddingsGenerator()
            )
            
            self.logger.info("Created new session with ID: %s", session_id)
            return session_id
            
        except Exception as e:
            self.logger.error("Failed to create session: %s", e)
            raise RuntimeError(f"Failed to create session: {str(e)}") from e
    
    def send_message(self, session_id: str, message: str) -> Message:
        """
        Send a message to a session and get the response.

        Args:
            session_id (str): The ID of the session to send the message to.
            message (str): The content of the message.

        Returns:
            Message: The response from the model.
            
        Raises:
            ValueError: If session_id is invalid or message is empty.
            RuntimeError: If message processing fails.
        """
        if not session_id or not session_id.strip():
            self.logger.error("Invalid session ID provided")
            raise ValueError("session_id cannot be empty or None")
            
        if not message or not message.strip():
            self.logger.error("Empty message provided")
            raise ValueError("message cannot be empty or None")
            
        if session_id not in self.sessions:
            self.logger.error("Session not found: %s", session_id)
            raise ValueError(f"Session with ID {session_id} does not exist")
        
        try:
            session = self.sessions[session_id]
            self.logger.info("Processing message for session: %s", session_id)
            
            # Add user message to session
            session.add_message(role="user", content=message)
            
            # Generate and return response
            response = session.generate_response(prompt=message)
            return response
            
        except Exception as e:
            self.logger.error("Error processing message for session %s: %s", session_id, e)
            raise RuntimeError(f"Failed to process message: {str(e)}") from e
    
    def get_history(self, session_id: str) -> List[Message]:
        """
        Get message history for a session.

        Args:
            session_id (str): The ID of the session to get history from.

        Returns:
            List[Message]: The message history of the session.
            
        Raises:
            ValueError: If session_id is invalid or does not exist.
        """
        if not session_id or not session_id.strip():
            self.logger.error("Invalid session ID provided")
            raise ValueError("session_id cannot be empty or None")
            
        if session_id not in self.sessions:
            self.logger.error("Session not found: %s", session_id)
            raise ValueError(f"Session with ID {session_id} does not exist")
        
        self.logger.debug("Retrieving history for session: %s", session_id)
        return self.sessions[session_id].get_history()
    
    def close_session(self, session_id: str) -> bool:
        """
        Close a chat session.

        Args:
            session_id (str): The ID of the session to close.

        Returns:
            bool: True if the session was closed, False if it did not exist.
        """
        if not session_id or not session_id.strip():
            self.logger.error("Invalid session ID provided")
            return False
            
        if session_id not in self.sessions:
            self.logger.debug("Session not found for closing: %s", session_id)
            return False
        
        try:
            # Call the session's close method first
            if hasattr(self.sessions[session_id], 'close'):
                self.sessions[session_id].close()
                
            # Then remove it from our dictionary
            del self.sessions[session_id]
            self.logger.info("Closed session: %s", session_id)
            return True
            
        except Exception as e:
            self.logger.error("Error closing session %s: %s", session_id, e)
            return False
    
    def shutdown(self):
        """
        Gracefully shutdown the service.
        
        Closes all sessions and clients, and performs necessary cleanup.
        """
        self.logger.info("Shutting down ABIOService")
        
        # Close all sessions
        for session_id in list(self.sessions.keys()):
            try:
                self.close_session(session_id)
            except Exception as e:
                self.logger.error("Error closing session %s during shutdown: %s", session_id, e)
            
        # Close all clients
        for model_name, client in list(self.clients.items()):
            try:
                client.close()
                self.logger.info("Closed client: %s", model_name)
            except Exception as e:
                self.logger.error("Error closing client %s during shutdown: %s", model_name, e)
            
        self.logger.info("ABIOService shut down successfully")
    
    def reload_config(self) -> bool:
        """
        Reload service configuration.
        
        Returns:
            bool: True if config was reloaded successfully, False otherwise.
        """
        try:
            # ConfigManager doesn't have a reload parameter, so create a new instance
            self.config_manager = ConfigManager(config_path=self.config_path)
            self.config = self.config_manager.get_config()
            self.logger.info("Configuration reloaded successfully")
            return True
        except Exception as e:
            self.logger.error("Error reloading configuration: %s", e)
            return False
            
    def get_active_sessions(self) -> List[str]:
        """
        Get list of active session IDs.
        
        Returns:
            List[str]: List of active session IDs.
        """
        self.logger.debug("Retrieving %d active sessions", len(self.sessions))
        return list(self.sessions.keys())
    
    def close(self) -> None:
        """
        Performs cleanup for the ABIOService.
        
        This is an alias for shutdown() for consistency with other components.
        """
        self.shutdown()