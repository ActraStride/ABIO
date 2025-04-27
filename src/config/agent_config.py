"""
Module Name: agent_config

Manages the application configuration for the Abio agent.

This module provides the ConfigManager class, responsible for:
- Loading configuration from YAML files (Abiofiles) or using default settings.
- Providing access to configuration values.
- Updating and saving configuration changes.

Example:
    >>> from src.config.agent_config import ConfigManager
    >>> config_manager = ConfigManager(config_path="abio.yaml")
    >>> config = config_manager.get_config()
    >>> print(config.agent.name)

Dependencies:
    - logging
    - yaml
    - pydantic
    - src.models.config (AbioConfig)
"""

import logging
import yaml
from typing import Optional
from pydantic import ValidationError
from src.models.config import AbioConfig

class ConfigManager:
    def __init__(self, config_path: Optional[str] = None, config: Optional[AbioConfig] = None): 
        """
        Initializes the ConfigManager.

        Loads the configuration from:
            1. A provided `AbioConfig` object (if given).
            2. A YAML file specified by `config_path` (if given).
            3. Default configuration values if neither `config` nor `config_path` are provided.

        Args:
            config_path (Optional[str]): Path to the Abio configuration file (YAML format).
                                         If provided, the configuration will be loaded from this file.
            config (Optional[AbioConfig]): An existing AbioConfig object.
                                          If provided, this configuration object will be used directly.

        Raises:
            FileNotFoundError: If `config_path` is provided but the file does not exist.
            ValueError: If there are issues loading or parsing the configuration file.
            yaml.YAMLError: If the YAML file is not properly formatted.
            ValidationError: If the loaded data does not match the AbioConfig schema.
        """
        self.logger = logging.getLogger(__name__) # Initialize logger for this class
        self.logger.info("Initializing ConfigManager.")

        self._config = None  # Initialize config attribute
        self._config_path = config_path # Store config path, even if not used immediately

        if config:
            self.logger.info("Using provided AbioConfig object.")
            self._config = config
        elif config_path:
            self.logger.info("Loading configuration from file: %s", config_path)
            try:
                self._config = self._load_from_file(config_path)
            except FileNotFoundError as e:
                self.logger.error("Configuration file not found: %s", config_path)
                raise # Re-raise to propagate the exception
            except ValueError as e:
                self.logger.error("Error loading configuration from file %s: %s", config_path, e)
                raise # Re-raise to propagate the exception
        else:
            self.logger.info("Creating default configuration.")
            self._config = self._create_default_config()

        self.logger.info("ConfigManager initialized successfully.")

    def get_config(self) -> AbioConfig: 
        """
        Returns the current configuration object.

        Returns:
            AbioConfig: The current configuration object.
        """
        self.logger.debug("Retrieving configuration.")
        return self._config

    def update_config(self, new_config: AbioConfig) -> None: 
        """
        Updates the current configuration object with a new configuration.

        Args:
            new_config (AbioConfig): The new configuration object to set as the current configuration.
        """
        self.logger.info("Updating configuration.")
        self._config = new_config
        self.logger.info("Configuration updated successfully.")

    def save_config(self, path: Optional[str] = None) -> None:
        """
        Persists the current configuration to a YAML file.

        If a `path` is provided, the configuration will be saved to that path.
        Otherwise, it will be saved to the original `config_path` used during initialization,
        if one was provided.

        Args:
            path (Optional[str]):  Optional path to save the configuration file.
                                   If None, saves to the original `config_path` (if available).

        Raises:
            ValueError: If no path is specified for saving and no original `config_path` was provided during initialization.
            IOError: If there is an error writing to the file.
            yaml.YAMLError: If there is an error serializing the config to YAML.
        """
        save_path = path or self._config_path
        if not save_path:
            self.logger.error("No path specified for saving configuration and no original config_path available.")
            raise ValueError("No path specified for saving configuration")

        self.logger.info("Saving configuration to: %s", save_path)
        try:
            config_dict = self._config.model_dump()
            with open(save_path, 'w') as f:
                yaml.safe_dump(config_dict, f)
            self.logger.info("Configuration saved successfully to: %s", save_path)

        except IOError as e:
            self.logger.error("Error saving configuration to %s: %s", save_path, e)
            raise IOError(f"Error saving configuration to {save_path}: {e}") from e
        except Exception as e: # Catch-all for other potential errors during saving
            self.logger.error("Unexpected error while saving configuration to %s: %s", save_path, e)
            raise RuntimeError(f"Unexpected error saving configuration to {save_path}: {e}") from e

    def _load_from_file(self, path: str) -> AbioConfig:
        """
        Loads and validates configuration from a YAML file using model_validate.

        Args:
            path (str): The path to the YAML configuration file.

        Returns:
            AbioConfig: An instance of AbioConfig with the loaded configuration.

        Raises:
            FileNotFoundError: If the configuration file does not exist.
            yaml.YAMLError: If the YAML file is not properly formatted.
            ValidationError: If the loaded data does not match the AbioConfig schema.
        """
        try:
            self.logger.debug("Loading configuration from file: %s", path)
            with open(path, 'r') as f:
                config_dict = yaml.safe_load(f) # Use safe_load to prevent arbitrary code execution
        except FileNotFoundError:
            self.logger.error("Configuration file not found at: %s", path)
            raise 
        except yaml.YAMLError as e:
            self.logger.error("Error parsing YAML file at %s: %s", path, e)
            raise 

        try:
            config = AbioConfig.model_validate(config_dict) # Use model_validate instead of parse_obj
            self.logger.info("Configuration loaded and validated successfully.")
            self.logger.debug("Loaded configuration: %s", config) # Log the loaded config in debug mode
            return config
        except ValidationError as e:
            self.logger.error("Configuration validation error: %s", e)
            raise 

    def _create_default_config(self) -> AbioConfig:
        """
        Creates a default configuration when no config file or object is provided.
        
        Returns:
            AbioConfig: A default configuration object.
        """
        self.logger.debug("Creating default configuration.")
        return AbioConfig(
            agent={
                "name": "Abio",
                "version": "1.0.0",
                "description": "AI agent for conversational tasks.",
                "environment": "development"
            },
            chat={
                "default_model": "models/gemini-1.5-flash",
                "temperature": 0.7,
                "top_p": 0.9
            },
            context={
                "message_limit": 10,
                "initial_prompts": [
                    {"role": "system", "content": "You are a helpful agent."},
                    {"role": "user", "content": "Hello, who are you?"}
                ]
            },
            meta={
                "created_by": "YourName",
                "created_at": "2025-04-13",
                "last_updated": "2025-04-13"
            }
        )
        
    def close(self) -> None:
        """
        Performs cleanup for the ConfigManager.
        
        This method is a placeholder for any cleanup logic that might be needed
        in the future for consistency with other components.
        """
        try:
            self.logger.info("Closing ConfigManager.")
            # Add any cleanup logic here if needed in the future
        except Exception as e:
            self.logger.error("Error during ConfigManager cleanup: %s", e)
