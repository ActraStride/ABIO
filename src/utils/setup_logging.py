"""
Module Name: setup_logging

Advanced logging configuration for Python applications.

This module provides centralized logging configuration, including:
- Log file rotation
- Secure directory setup
- Robust error handling
- Consistent UTC timezone formatting

Example:
    >>> from src.utils import setup_logging
    >>> setup_logging()
    >>> logger = logging.getLogger(__name__)
    >>> logger.info("Hello, world!")
"""

import logging.config
import time
import sys

from pathlib import Path
from typing import Final
from logging.handlers import RotatingFileHandler

from src.errors.core import * 

# Immutable constants (type hinted)
LOG_DIR_NAME: Final[str] = "logs"
LOG_FILE_NAME: Final[str] = "application.log"
LOG_FORMAT: Final[str] = (
    "%(asctime)s.%(msecs)03d [%(levelname)-8s] "
    "%(name)s:%(funcName)s:%(lineno)d - %(message)s"
)
LOG_DATE_FORMAT: Final[str] = "%Y-%m-%dT%H:%M:%S%z"
LOG_MAX_BYTES: Final[int] = 10 * 1024 * 1024  # 10 MB
LOG_BACKUP_COUNT: Final[int] = 5
LOG_ENCODING: Final[str] = "utf-8"


def get_log_dir(project_root: Path = None) -> Path:
    """
    Safely determines and creates the log directory.

    Args:
        project_root (Path, optional): Root path of the project. Defaults to None.

    Returns:
        Path: Absolute path to the log directory.

    Raises:
        LoggingSetupError: If the directory cannot be created.
    """
    try:
        if project_root is None:
            # Assumes this file is located in project_root/src/utils
            project_root = Path(__file__).resolve().parent.parent.parent
            
        log_dir = project_root / LOG_DIR_NAME
        log_dir.mkdir(parents=True, exist_ok=True)
        return log_dir
    except (PermissionError, FileExistsError, OSError) as e:
        raise LoggingSetupError(
            f"Failed to create log directory: {e}"
        ) from e

def get_logging_config(log_file_path: Path, log_level: str) -> dict:
    """
    Generates dynamic logging configuration with type hints and validation.

    Args:
        log_file_path (Path): Full path to the log file.
        log_level (str): Logging level (e.g., "DEBUG", "INFO", "WARNING").

    Returns:
        dict: Logging configuration compatible with `dictConfig`.
    """
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": LOG_FORMAT,
                "datefmt": LOG_DATE_FORMAT,
                "validate": True,
            }
        },
        "handlers": {
            "rotating_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": log_level,
                "formatter": "standard",
                "filename": str(log_file_path),
                "encoding": LOG_ENCODING,
                "maxBytes": LOG_MAX_BYTES,
                "backupCount": LOG_BACKUP_COUNT,
                "delay": True,  # Delays file opening until first use
            },
            "console": {
                "class": "logging.StreamHandler",
                "level": "WARNING",
                "formatter": "standard",
                "stream": sys.stdout,
            },
        },
        "loggers": {
            # Root logger configures all modules
            "": {
                "handlers": ["rotating_file", "console"],
                "level": log_level,
                "propagate": False,
            },
            # Specific configuration for noisy dependencies
            "urllib3": {
                "level": "WARNING",
                "propagate": False,
            },
        },
    }

def setup_logging(log_level: str, project_root: Path = None) -> None:
    """
    Configures the application's logging system.

    Args:
        log_level (str): Logging level (e.g., "DEBUG", "INFO", "WARNING").
        project_root (Path, optional): Root directory of the project. Defaults to None.

    Raises:
        ValueError: If an invalid log level is provided.
        LoggingSetupError: If logging configuration fails.
    """
    try:
        if log_level not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
            raise ValueError(f"Invalid log level: {log_level}")
        
        # Get log directory
        log_dir = get_log_dir(project_root)
        log_file = log_dir / LOG_FILE_NAME
        
        # Configure logging
        config = get_logging_config(log_file, log_level)
        logging.config.dictConfig(config)
        
        # Set UTC for log timestamps (or local time if preferred)
        logging.Formatter.converter = time.localtime  # Use local time
        
        # Log success
        logger = logging.getLogger(__name__)
        logger.info(
            "Logging configured successfully. File: %s", log_file
        )
        
        print(f"Log directory: {log_dir}")
    
    except ValueError as ve:
        logging.error("Invalid log level provided: %s", ve)
        raise
    except Exception as e:
        logging.error("Error setting up logging system: %s", e)
        raise LoggingSetupError(
            f"Error setting up logging system: {e}"
        ) from e