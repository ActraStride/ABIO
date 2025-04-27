import logging
import uuid
from pathlib import Path
from typing import Dict, List, Optional

from src.clients.gemini_client import GeminiClient
from src.utils.setup_logging import setup_logging
from src.chat.chat_session import ChatSession
from src.config.agent_config import ConfigManager
from src.context import ContextManager
from src.embeddings import EmbeddingsGenerator
from src.models.message import Message


class ABIOService:
    """Service layer for ABIO chat system that encapsulates all core functionality."""
    
    def __init__(self, config_path: str = "Abiofile"):
        """Initialize service with configuration path."""
        self.config_path = config_path
        self.config_manager = None
        self.config = None
        self.clients: Dict[str, GeminiClient] = {}
        self.sessions: Dict[str, ChatSession] = {}
        self.logger = logging.getLogger("ABIOService")
        
    def initialize(self):
        """Initialize the service and required resources."""
        # Setup logging
        setup_logging(log_level="INFO", project_root=Path("/home/actra_dev/Desktop/ABIO"))
        
        # Load configuration
        self.config_manager = ConfigManager(config_path=self.config_path)
        self.config = self.config_manager.get_config()
        self.logger.info("📄 Configuration loaded from %s", self.config_path)
        
        # Initialize default client
        self._init_default_client()
        return self
        
    def _init_default_client(self):
        """Initialize the default model client."""
        model_name = self.config.chat.default_model
        self.clients[model_name] = GeminiClient(model_name=model_name)
        self.logger.info("🤖 Initialized default model client: %s", model_name)
        
    def create_session(self, user_id: Optional[str] = None) -> str:
        """Create a new chat session and return its ID."""
        session_id = str(uuid.uuid4())
        
        # Get the default client 
        model_name = self.config.chat.default_model
        client = self.clients[model_name]
        
        # Initialize session components
        context_manager = ContextManager(
            self.config.context.message_limit, 
            self.config.context.context_messages
        )
        
        # Create chat session
        self.sessions[session_id] = ChatSession(
            session_id=session_id,
            client=client,
            context_manager=context_manager,
            embeddings_generator=EmbeddingsGenerator()
        )
        
        self.logger.info("✅ Created new session with ID: %s", session_id)
        return session_id
    
    def send_message(self, session_id: str, message: str) -> Message:
        """Send a message to a session and get the response."""
        if session_id not in self.sessions:
            self.logger.error("Session not found: %s", session_id)
            raise ValueError(f"Session with ID {session_id} does not exist")
        
        session = self.sessions[session_id]
        self.logger.info("💬 Processing message for session: %s", session_id)
        
        # Add user message to session
        session.add_message(role="user", content=message)
        
        # Generate and return response
        response = session.generate_response(prompt=message)
        return response
    
    def get_history(self, session_id: str) -> List[Message]:
        """Get message history for a session."""
        if session_id not in self.sessions:
            self.logger.error("Session not found: %s", session_id)
            raise ValueError(f"Session with ID {session_id} does not exist")
        
        return self.sessions[session_id].get_history()
    
    def close_session(self, session_id: str) -> bool:
        """Close a chat session."""
        if session_id not in self.sessions:
            return False
        
        # Perform any cleanup needed
        del self.sessions[session_id]
        self.logger.info("🔒 Closed session: %s", session_id)
        return True
    
    def shutdown(self):
        """Gracefully shutdown the service."""
        # Close all sessions
        for session_id in list(self.sessions.keys()):
            self.close_session(session_id)
            
        # Close all clients
        for client in self.clients.values():
            client.close()
            
        self.logger.info("👋 ABIO Service shut down successfully")
    
    def reload_config(self) -> bool:
        """Reload service configuration."""
        try:
            self.config = self.config_manager.get_config(reload=True)
            self.logger.info("🔄 Configuration reloaded successfully")
            return True
        except Exception as e:
            self.logger.error("Error reloading configuration: %s", str(e))
            return False
            
    def get_active_sessions(self) -> List[str]:
        """Get list of active session IDs."""
        return list(self.sessions.keys())