"""
Custom exceptions for the Portfolio Email API.
"""


class EmailServiceError(Exception):
    """Base exception for email service errors."""
    pass


class EmailConfigurationError(EmailServiceError):
    """Raised when email service is not properly configured."""
    pass


class EmailSendError(EmailServiceError):
    """Raised when email fails to send."""
    pass


class ContactSaveError(Exception):
    """Raised when contact fails to save to JSON."""
    pass
