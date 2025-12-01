"""
FastAPI application for portfolio contact forms.
Production-ready with modular architecture.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import router
from app.core import get_settings, setup_logging, get_logger
from app.middleware import log_requests_middleware

# Setup logging
setup_logging()
logger = get_logger(__name__)

# Get settings
settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title="Portfolio Email API",
    description="Professional email service for portfolio contact forms",
    version="1.0.0"
)

# Add request logging middleware
app.middleware("http")(log_requests_middleware)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)

# Startup event
@app.on_event("startup")
async def startup_event():
    """Log startup information."""
    logger.info(f"Portfolio Email API started")
    logger.info(f"CORS Origins: {settings.cors_allow_origin}")
    logger.info(f"Email Provider: {'Resend' if settings.resend_api_key else 'SMTP'}")
    logger.info(f"Dry Run Mode: {settings.email_dry_run}")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Log shutdown information."""
    logger.info("Portfolio Email API shutting down")
