"""
Core package initialization.
"""

from .config import Settings, get_settings
from .logging import setup_logging, get_logger
from .exceptions import (
    EmailServiceError,
    EmailConfigurationError,
    EmailSendError,
    ContactSaveError
)

__all__ = [
    "Settings",
    "get_settings",
    "setup_logging",
    "get_logger",
    "EmailServiceError",
    "EmailConfigurationError",
    "EmailSendError",
    "ContactSaveError"
]