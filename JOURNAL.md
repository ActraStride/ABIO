# JOURNAL.md

## Add Configuration Management for Chat Agent Settings [#4]

### Objective

**Research how to use the parameters from the current configuration file (see below) to build a configuration management module.**  
This module should contain functions that construct the configuration object to be shared across different components via the service module.

### Configuration File Example (`Abiofile`)

```yaml
# General configuration file for the AI agent - Abiofile

agent:
  name: "<AGENT_NAME>"                          # (str) Name of the AI agent.
  version: "<VERSION>"                          # (str) Version number of the agent (e.g., 1.0.0).
  description: "<AGENT_DESCRIPTION>"            # (str) Brief description of the agent’s functionality.
  environment: "<development|production|test>"  # (str) Environment in which the agent is running.

chat:
  message_limit: <CONTEXT_MESSAGE_LIMIT>        # (int) Maximum number of messages to retain in the conversation context (e.g., 50).
  default_model: "<AI_MODEL_NAME>"              # (str) Default AI model name (e.g., gemini-1.5-flash).
  temperature: <FLOAT_VALUE_BETWEEN_0_AND_1>    # (float) Sampling temperature to control randomness. Higher values = more creative.
  top_p: <FLOAT_VALUE_BETWEEN_0_AND_1>          # (float) Nucleus sampling parameter. Lower values = more focused output.

  pretraining_prompts:
    - role: "system"                            # (str) Role of the speaker. Use "system" to define initial behavior.
      content: "<INITIAL_SYSTEM_MESSAGE>"       # (str) Initial instructions or system rules for the AI.
    - role: "user"                              # (str) Role of the user initiating the first interaction.
      content: "<INITIAL_USER_QUESTION>"        # (str) Initial question or prompt to guide the agent’s behavior.

meta:
  created_by: "<YOUR_NAME>"                     # (str) Author or creator of the configuration file.
  created_at: "<CREATION_DATE>"                 # (str) Date the file was created (e.g., 2025-04-13).
  last_updated: "<LAST_UPDATE_DATE>"            # (str) Date of the last modification to the file.
```

---

### What Is an `ABIO_CONFIG_OBJECT` and How Is It Built?

The `ABIO_CONFIG_OBJECT` is a standardized format used to build the AI agent, its **pretraining behavior**, and **memory**, along with other essential settings such as:

- Conversation limits  
- Model selection  
- Temperature and sampling settings  
- Additional metadata

The configuration module must be capable of building this object from the `abio` configuration file **or independently** (without requiring the file).

---

### Development of the `CONFIG_MANAGER` Class

The `CONFIG_MANAGER` class presents several open questions, such as:

- How should the configuration object be handled?
- Is it appropriate to place it inside the `models` folder?
- How should the configuration object be structured?
- What should the structure of the `CONFIG_MANAGER` class look like?

Below is a basic prototype to explore these questions:

---

### Primitive Version of the `AbioConfig` Class

```python
class AbioConfig:
    def __init__(self, agent, chat, meta):
        self.agent = agent
        self.chat = chat
        self.meta = meta

    def to_dict(self):
        """
        Converts the configuration object into a dictionary.
        """
        return {
            'agent': self.agent,
            'chat': self.chat,
            'meta': self.meta
        }
```

---

### Prototype of the `ConfigManager` Class

```python
import yaml

class ConfigManager:
    _config_instance = None  # Singleton pattern: holds the single instance of the configuration

    @staticmethod
    def load_configuration(file_path=None):
        """
        Loads the configuration from a YAML file or creates a default one if no file is provided.
        """
        if file_path:
            return ConfigManager._load_from_file(file_path)
        else:
            return ConfigManager._create_default_config()

    @staticmethod
    def _load_from_file(file_path):
        """
        Loads configuration data from a YAML file and builds an AbioConfig object.
        """
        with open(file_path, 'r') as file:
            config_data = yaml.safe_load(file)

        return AbioConfig(
            agent=config_data['agent'],
            chat=config_data['chat'],
            meta=config_data['meta']
        )

    @staticmethod
    def _create_default_config():
        """
        Builds a default configuration if no config file is provided.
        """
        return AbioConfig(
            agent={
                "name": "Abio",
                "version": "1.0.0",
                "description": "AI Agent",
                "environment": "development"
            },
            chat={
                "message_limit": 50,
                "default_model": "gemini-1.5-flash",
                "temperature": 0.7,
                "top_p": 0.9,
                "pretraining_prompts": []
            },
            meta={
                "created_by": "User",
                "created_at": "2025-04-13",
                "last_updated": "2025-04-13"
            }
        )

    @staticmethod
    def update_configuration(new_config, file_path='abiofile.yaml'):
        """
        Updates the configuration in memory and optionally writes it to a file.
        """
        ConfigManager._config_instance = new_config
        with open(file_path, 'w') as file:
            yaml.dump(new_config.to_dict(), file)

    @staticmethod
    def get_config():
        """
        Returns the singleton instance of the configuration.
        """
        if ConfigManager._config_instance is None:
            ConfigManager._config_instance = ConfigManager.load_configuration('abiofile.yaml')
        return ConfigManager._config_instance
```
---


### Building and Using the `ABIO_CONFIG_OBJECT`

The previously provided `AbioConfig` class must be restructured to fully represent **all configurable values** defined in an `abiofile`. 

#### Current Limitation

Currently, the configuration model only includes the following sections:
- `agent`
- `chat`
- `meta`

However, the `abiofile` contains additional important data that is not properly or completely represented in the current prototype, including:

- **Pretraining prompts**: These include defined roles such as `"system"` and `"user"`, with corresponding initial messages.
- **Model parameters**: Such as `default_model`, `temperature`, `top_p`, and `message_limit`.
- **Role-based structures**: The prompts use a `role` attribute, which may require more robust representation (e.g., using dedicated classes or enums instead of plain strings).

#### Required Improvements

- Define nested models to ensure that each section of the config is represented correctly and can be validated.
- Consider modeling pretraining prompts using a class like `PretrainingPrompt`, with typed fields: `role` and `content`.
- Ensure all default values are clearly specified and can be overridden.
- Optionally, use a schema validation library such as **Pydantic** to guarantee structural correctness and support typing, defaulting, and validation.

### Enhanced `AbioConfig` Class

```python
"""
Module: config

Defines the configuration models for the Abio AI agent.

This module provides Pydantic models to structure, validate, and manage
configuration data loaded from an Abiofile (YAML or JSON). The configuration
includes agent metadata, chat settings, and pretraining prompts.

Example:
    >>> from src.models.config import AbioConfig
    >>> config = AbioConfig.parse_file("abiofile.yaml")
    >>> print(config.agent.name)

Dependencies:
    - pydantic
    - typing
    - datetime
"""

from pydantic import BaseModel, Field
from typing import List, Literal, Optional
from datetime import datetime


class AgentConfig(BaseModel):
    """
    Configuration for the AI agent.

    Attributes:
        name (str): Name of the agent.
        version (str): Agent version (e.g., 1.0.0).
        description (str): Short description of the agent.
        environment (Literal): Runtime environment.
    """
    name: str
    version: str
    description: str
    environment: Literal["development", "production", "test"]

    class Config:
        from_attributes = True


class PretrainingPrompt(BaseModel):
    """
    Defines a single pretraining prompt with an assigned role.

    Attributes:
        role (Literal): Role of the message sender (e.g., system, user).
        content (str): Message content.
    """
    role: Literal["system", "user"]
    content: str

    class Config:
        from_attributes = True


class ChatConfig(BaseModel):
    """
    Configuration related to chat behavior and model parameters.

    Attributes:
        message_limit (int): Number of context messages.
        default_model (str): Name of the default model.
        temperature (float): Sampling temperature.
        top_p (float): Nucleus sampling value.
        pretraining_prompts (List[PretrainingPrompt]): Initial prompts.
    """
    message_limit: int = Field(..., ge=1)
    default_model: str
    temperature: float = Field(..., ge=0.0, le=1.0)
    top_p: float = Field(..., ge=0.0, le=1.0)
    pretraining_prompts: List[PretrainingPrompt] = []

    class Config:
        from_attributes = True


class MetaConfig(BaseModel):
    """
    Metadata for configuration creation and versioning.

    Attributes:
        created_by (str): Author of the configuration.
        created_at (str): ISO date of creation.
        last_updated (str): ISO date of last update.
    """
    created_by: str
    created_at: str
    last_updated: str

    class Config:
        from_attributes = True


class AbioConfig(BaseModel):
    """
    Root configuration model for the Abio agent.

    Attributes:
        agent (AgentConfig): General info and runtime environment.
        chat (ChatConfig): Chat parameters and prompts.
        meta (MetaConfig): Metadata about the config file.
    """
    agent: AgentConfig
    chat: ChatConfig
    meta: MetaConfig

    class Config:
        from_attributes = True

```

---

### Configuration Models and Loader Architecture

The configuration system for this project is designed to ensure strong validation, modularity, and scalability. It follows a structured approach using **Pydantic models** to represent and validate each section of the `abiofile` configuration file.

#### 🧩 Model Structure

All configuration-related classes are defined in `src/config/config.py`. The file contains nested data models representing each major section of the `abiofile`, including:

- **`AgentConfig`**: Describes the AI agent’s identity and operational context (e.g., `name`, `version`, `environment`).
- **`ChatConfig`**: Encapsulates model parameters such as `temperature`, `top_p`, `message_limit`, and the selected `default_model`.
- **`PretrainingPrompt`**: Represents initial prompts that define the conversation's behavior based on role (`system`, `user`).
- **`MetaConfig`**: Stores metadata like the author's name and timestamps for creation and last update.
- **`AbioConfig`**: The top-level model that aggregates all the sections above into a unified configuration object.

All models use type annotations and optional values to make the structure easy to validate, extend, and document. Here’s an example of the structure:

```python
class PretrainingPrompt(BaseModel):
    role: Literal["system", "user"]
    content: str

class ChatConfig(BaseModel):
    message_limit: int
    default_model: str
    temperature: float
    top_p: float
    pretraining_prompts: List[PretrainingPrompt]

class AbioConfig(BaseModel):
    agent: AgentConfig
    chat: ChatConfig
    meta: MetaConfig
```

Each model is written in accordance with the project’s code style, using full docstrings and Pydantic’s validation features.

#### ⚙️ Config Loader Module

The logic for reading and building the `AbioConfig` object from a YAML file is implemented in a dedicated loader function, currently stored in `src/config/config.py`.

However, for better separation of concerns, this loader may optionally be moved to `src/utils/helpers.py` or a specialized `src/config/loader.py` module if it grows in complexity.

```python
def load_abio_config(path: str) -> AbioConfig:
    with open(path, "r") as f:
        data = yaml.safe_load(f)
    return AbioConfig(**data)
```

This loader guarantees that any invalid structure or missing required field in the YAML file will raise an error early, preventing silent failures or misconfigurations at runtime.

> ✅ **Best Practice**: Keep model definitions inside the `config` package and abstract loading logic into a reusable utility function.

This system allows the configuration to be:
- Cleanly validated
- Easy to test
- Extensible for future settings

---

## Configuration Manager Development [#4]

### Objective

**Design and implement a comprehensive ConfigManager module to handle loading, accessing, and maintaining configuration settings across the Abio agent.**  
This module will extend the initial concepts into a robust system that properly encapsulates configuration management with clear responsibilities and integration points.

### Proposed `ConfigManager` Architecture

After reviewing the initial prototype and considering the system requirements, I've decided to develop a dedicated `ConfigManager` module rather than just helper functions. This approach will provide better encapsulation, state management, and integration with other components.

#### Key Design Decisions

1. **Separation of Models and Management Logic**: 
   - Keep Pydantic models in `config.py` for data structure and validation
   - Create a new `config_manager.py` with the `ConfigManager` class to handle loading, access, and persistence

2. **Responsibility Boundaries**:
   - The `ConfigManager` will be responsible for loading, caching, providing access to, and persisting configuration
   - The Pydantic models will handle validation and provide type safety
   - Service components will receive configuration via dependency injection

3. **No Global State**: Replace the singleton pattern with proper dependency injection to improve testability and flexibility

---

### ConfigManager Class Design

The `ConfigManager` will be implemented in `src/config/config_manager.py` with the following structure:

```python
class ConfigManager:
    """
    Manages the configuration lifecycle for the Abio agent.
    
    This class handles loading configuration from files or defaults,
    providing access to configuration values, and persisting changes.
    """
    
    def __init__(self, config_path: Optional[str] = None, config: Optional[AbioConfig] = None):
        """
        Initialize the config manager with either a file path or an existing config.
        
        Args:
            config_path: Path to an Abiofile (YAML)
            config: Pre-existing AbioConfig object
        """
        self._config = None
        self._config_path = config_path
        
        if config:
            self._config = config
        elif config_path:
            self._config = self._load_from_file(config_path)
        else:
            self._config = self._create_default_config()
    
    def get_config(self) -> AbioConfig:
        """Returns the current configuration object."""
        return self._config
    
    def update_config(self, new_config: AbioConfig) -> None:
        """Updates the current configuration object."""
        self._config = new_config
        
    def save_config(self, path: Optional[str] = None) -> None:
        """
        Persists the current configuration to a file.
        
        Args:
            path: Path to save the configuration (defaults to original path)
        """
        save_path = path or self._config_path
        if not save_path:
            raise ValueError("No path specified for saving configuration")
            
        # Implementation for serializing and saving config
        
    # Private methods
    def _load_from_file(self, path: str) -> AbioConfig:
        """Loads and validates configuration from a file."""
        # Implementation

    def _create_default_config(self) -> AbioConfig:
        """Creates a default configuration object."""
        # Implementation
```

---

### Integration with Service Layer

The `ConfigManager` will be integrated with the service layer, particularly `AbioService`, to provide configuration access to other components. This eliminates the need for global state while ensuring components have access to the configuration they need.

```python
class AbioService:
    """
    Core service class for the Abio agent that coordinates components
    and provides access to configuration.
    """
    
    def __init__(self, config_manager: ConfigManager):
        """
        Initialize the service with a configuration manager.
        
        Args:
            config_manager: Configuration manager instance
        """
        self._config_manager = config_manager
        self._chat_session = None
        self._model_client = None
        
        # Initialize components with configuration
        self._initialize_components()
        
    def _initialize_components(self):
        """Initialize component services with appropriate config."""
        config = self._config_manager.get_config()
        
        # Initialize model client with model config
        self._model_client = self._create_model_client(config.chat.default_model)
        
        # Initialize chat session with message limits and pretraining prompts
        self._chat_session = ChatSession(
            message_limit=config.chat.message_limit,
            pretraining_prompts=config.chat.pretraining_prompts
        )
        
    def _create_model_client(self, model_name: str):
        """Create the appropriate model client based on config."""
        # Implementation for client selection
```

---

### Configuration Change Handling

One important consideration is how to handle configuration changes during runtime. Here's the proposed approach:

1. **Observable Configuration Changes**:
   - Implement an event notification system for configuration changes
   - Allow components to register for notifications about specific config changes
   
2. **Dynamic Reconfiguration**:
   - Define which components can be reconfigured at runtime
   - Provide methods for controlled updates to avoid inconsistent states

3. **Validation Before Changes**:
   - Validate any configuration changes before applying them
   - Maintain an audit log of configuration changes

```python
# Pseudocode for config change handling
class ConfigManager:
    # ... existing methods ...
    
    def register_change_listener(self, listener: Callable[[str, Any, Any], None]) -> None:
        """Register a listener for configuration changes."""
        self._listeners.append(listener)
        
    def update_value(self, path: str, value: Any) -> None:
        """
        Update a specific configuration value and notify listeners.
        
        Args:
            path: Dot-notation path to the configuration value
            value: New value to set
        """
        # Get old value
        old_value = self._get_value_by_path(path)
        
        # Apply the change
        self._set_value_by_path(path, value)
        
        # Notify listeners
        for listener in self._listeners:
            listener(path, old_value, value)
```

---

### Environment-specific Configuration

The configuration system should support different environments as specified in the `agent.environment` field. Here's how this will be implemented:

1. **Environment Configuration Files**:
   - Support loading base configuration plus environment-specific overrides
   - Use naming convention: `abiofile.yaml`, `abiofile.development.yaml`, etc.

2. **Configuration Merging**:
   - Implement deep merging of configuration objects
   - Allow specific values to be overridden while maintaining defaults

```python
def load_environment_config(base_path: str, environment: str) -> AbioConfig:
    """
    Load configuration with environment-specific overrides.
    
    Args:
        base_path: Path to the base configuration file
        environment: Environment name (development, production, test)
        
    Returns:
        Merged configuration object
    """
    # Load base config
    base_config = load_config(base_path)
    
    # Check for environment config
    env_path = f"{base_path.rsplit('.', 1)[0]}.{environment}.yaml"
    if os.path.exists(env_path):
        env_config = load_config(env_path)
        # Merge configurations
        return merge_configs(base_config, env_config)
    
    return base_config
```

---

### Future Considerations

Several aspects will need further development as the project evolves:

1. **Configuration Schema Versioning**:
   - Support for migrating between configuration schema versions
   - Backward compatibility handling

2. **Sensitive Data Management**:
   - Secure storage of API keys and other sensitive values
   - Environment variable integration for sensitive data

3. **Configuration Validation Rules**:
   - Custom validation rules beyond simple type checking
   - Inter-field dependencies and constraints

4. **Configuration Editor UI**:
   - Potential web interface for editing configuration
   - Schema-driven form generation

---

### Next Steps

1. Implement the core `ConfigManager` class with file loading and validation
2. Add support for environment-specific configurations
3. Integrate the configuration manager with the service layer
4. Develop automated tests for configuration loading and validation edge cases
5. Document the configuration system for other developers

With this architecture, the configuration system will provide a solid foundation for the Abio agent, ensuring that all components have access to properly validated configuration values while maintaining separation of concerns and testability.








<!-- 

CONTEMPLAR EN EL FUTURO

```yaml

memory:
  type: "<vector|redis|inmemory>"
  backend: "<faiss|pinecone|weaviate|custom>"
  persist: <true|false>
  path: "<RUTA_DE_ALMACENAMIENTO_LOCAL>"

logging:
  enabled: <true|false>
  level: "<debug|info|warning|error>"
  save_to_file: <true|false>
  log_file: "<RUTA_DEL_LOG>" # ej. ./logs/agent.log

api:
  enabled: <true|false>
  host: "<DIRECCION_IP>" # ej. 127.0.0.1
  port: <PUERTO>         # ej. 8000

security:
  anonymize_user_data: <true|false>
  allow_origins:
    - "<origen_1>"  # ej. http://localhost
    - "<origen_2>"

tools:
  - name: "<NOMBRE_DEL_TOOL>"  # ej. web_search
    enabled: <true|false>
  - name: "<NOMBRE_DEL_TOOL_2>"
    enabled: <true|false>

``` -->
