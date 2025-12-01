"""
Health check utilities for the application.
"""
from typing import Dict, Any
from app.core import get_settings


def get_health_status() -> Dict[str, Any]:
    """Get application health status."""
    settings = get_settings()
    
    return {
        "status": "healthy",
        "service": "Portfolio Email API",
        "version": "1.0.0",
        "email_provider": "resend" if settings.resend_api_key else "smtp",
        "dry_run_mode": settings.email_dry_run
    }


def get_config_status() -> Dict[str, Any]:
    """Get configuration status (without sensitive data)."""
    settings = get_settings()
    
    return {
        "resend_configured": bool(settings.resend_api_key),
        "smtp_configured": bool(settings.smtp_host and settings.smtp_user),
        "email_from_set": bool(settings.email_from),
        "email_to_set": bool(settings.email_to),
        "dry_run": settings.email_dry_run,
        "cors_origins": len(settings.cors_allow_origin)
    }
