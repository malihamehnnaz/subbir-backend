"""
Simple FastAPI application for portfolio contact forms.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import router
from app.core import get_settings, setup_logging, get_logger

# Setup logging
setup_logging()
logger = get_logger(__name__)

# Get settings
settings = get_settings()

# Log the platform-provided PORT (helpful for debugging deployments)
import os
logger.info(f"PORT env: {os.getenv('PORT')}")

# Create FastAPI app
app = FastAPI(
    title="Portfolio Email API",
    description="Simple API for portfolio contact forms with JSON logging"
)

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

# Log startup
logger.info(f"Portfolio Email API started. CORS: {settings.cors_allow_origin}")