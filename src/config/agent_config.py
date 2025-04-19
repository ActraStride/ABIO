"""
Module Name: config_manager

Manages the application configuration for the Abio agent.

This module provides the ConfigManager class, responsible for:
- Loading configuration from YAML files (Abiofiles) or using default settings.
- Providing access to configuration values.
- Updating and saving configuration changes.

Example:
    >>> from src.config_manager import ConfigManager
    >>> config_manager = ConfigManager(config_path="abio.yaml")
    >>> config = config_manager.get_config()
    >>> print(config.gemini_api_key)
"""

import logging
import yaml
from typing import Optional
from pydantic import ValidationError
from src.models import AbioConfig

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
            # Potentially other exceptions depending on serialization implementation (e.g., YAML library errors)
        """
        save_path = path or self._config_path
        if not save_path:
            self.logger.error("No path specified for saving configuration and no original config_path available.")
            raise ValueError("No path specified for saving configuration")

        self.logger.info("Saving configuration to: %s", save_path)
        try:
            # Implementation for serializing and saving config to YAML file (e.g., using yaml library)
            # Example (pseudocode - replace with actual YAML serialization):
            # with open(save_path, 'w') as f:
            #     yaml.dump(self._config.to_dict(), f) # Assuming AbioConfig can be converted to a dict
            pass # Placeholder for implementation
            self.logger.info("Configuration saved successfully to: %s", save_path)

        except IOError as e:
            self.logger.error("Error saving configuration to %s: %s", save_path, e)
            raise IOError(f"Error saving configuration to {save_path}: {e}") from e
        except Exception as e: # Catch-all for other potential errors during saving
            self.logger.error("Unexpected error while saving configuration to %s: %s", save_path, e)
            raise RuntimeError(f"Unexpected error saving configuration to {save_path}: {e}") from e


    # Private methods - starting with single underscore '_' is more common in Python for internal methods
    def _load_from_file(self, path: str) -> AbioConfig:
        """
        Loads and validates configuration from a YAML file using model_validate.

        Args:
            path (str): The path to the YAML configuration file.

        Returns:
            AbioConfig: An instance of AbioConfig with the loaded configuration.

        Raises:
            FileNotFoundError: If the configuration file does not exist.
            YAMLError: If the YAML file is not properly formatted.
            ValidationError: If the loaded data does not match the AbioConfig schema.
        """
        try:
            self.logger.debug(f"Loading configuration from file: {path}")
            with open(path, 'r') as f:
                config_dict = yaml.safe_load(f) # Use safe_load to prevent arbitrary code execution
        except FileNotFoundError:
            self.logger.error(f"Configuration file not found at: {path}")
            raise FileNotFoundError(f"Configuration file not found at: {path}")
        except yaml.YAMLError as e:
            self.logger.error(f"Error parsing YAML file at {path}: {e}")
            raise yaml.YAMLError(f"Error parsing YAML file at {path}: {e}")

        try:
            config = AbioConfig.model_validate(config_dict) # Use model_validate instead of parse_obj
            self.logger.info("Configuration loaded and validated successfully.")
            self.logger.debug(f"Loaded configuration: {config}") # Log the loaded config in debug mode
            return config
        except ValidationError as e:
            self.logger.error(f"Configuration validation error: {e}")
            raise ValidationError(f"Configuration validation error: {e}") from e # Re-raise with context

    def _create_default_config(self) -> AbioConfig:
        self.logger.debug("Creando configuración por defecto.")
        return AbioConfig(
            agent={
                "name": "Abio",
                "version": "1.0.0",
                "description": "Agente de IA para tareas conversacionales.",
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
                    {"role": "system", "content": "Eres un agente útil."},
                    {"role": "user", "content": "Hola, ¿quién eres?"}
                ]
            },
            meta={
                "created_by": "TuNombre",
                "created_at": "2025-04-13",
                "last_updated": "2025-04-13"
            }
        )
