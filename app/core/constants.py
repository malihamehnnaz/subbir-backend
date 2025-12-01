"""
Application constants and configuration values.
"""

# Application metadata
APP_NAME = "Portfolio Email API"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Professional email service for portfolio contact forms"

# Email configuration
DEFAULT_SMTP_PORT = 587
SMTP_SSL_PORT = 465

# File storage
DATA_DIR = "data"
CONTACTS_FILE_PREFIX = "contacts_"
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S UTC"

# Email subjects
EMAIL_SUBJECT_PREFIX = "💼 Portfolio Contact:"

# Retry configuration
MAX_RETRY_ATTEMPTS = 3
RETRY_MIN_WAIT = 1
RETRY_MAX_WAIT = 10
