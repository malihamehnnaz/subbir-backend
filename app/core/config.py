"""
Simple configuration for the Portfolio Email API.
"""

import os
from typing import List


class Settings:
    """Simple settings class that loads from environment variables."""
    
    def __init__(self):
        # API Settings
        self.app_name = "Portfolio Email API"
        self.version = "1.0.0"
        
        # CORS Settings
        cors_env = os.getenv("CORS_ALLOW_ORIGIN", "*")
        if cors_env.strip() == "*":
            self.cors_allow_origin = ["*"]
        else:
            self.cors_allow_origin = [origin.strip() for origin in cors_env.split(",") if origin.strip()]
        
        # Email Settings
        self.email_from = os.getenv("EMAIL_FROM", "")
        self.email_to = os.getenv("EMAIL_TO", "")
        self.email_dry_run = os.getenv("EMAIL_DRY_RUN", "false").lower() in ("true", "1", "yes")
        
        # SMTP Settings
        self.smtp_host = os.getenv("SMTP_HOST", "")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USER", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")


# Global settings instance
_settings = None

def get_settings() -> Settings:
    """Get application settings (singleton pattern)."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings