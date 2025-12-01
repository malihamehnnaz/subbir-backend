"""
API routes for the Portfolio Email API.
"""

from fastapi import APIRouter, BackgroundTasks, HTTPException
from app.core import get_logger
from app.core.health import get_health_status, get_config_status
from app.models import ContactRequest, ContactResponse
from app.services import email_service

logger = get_logger(__name__)
router = APIRouter()


@router.get("/")
async def health_check():
    """Health check endpoint with service information."""
    return get_health_status()


@router.get("/health")
async def detailed_health():
    """Detailed health check with configuration status."""
    return {
        **get_health_status(),
        "config": get_config_status()
    }


@router.post("/send", status_code=202)
async def send_contact_email(
    contact: ContactRequest,
    background_tasks: BackgroundTasks
) -> ContactResponse:
    """
    Accept contact form submissions.
    Saves to JSON and optionally sends email in background.
    """
    # Schedule background processing
    background_tasks.add_task(
        process_contact,
        contact.name,
        contact.email,
        contact.message
    )
    
    return ContactResponse(
        status="accepted",
        message="Your message has been received and will be processed shortly."
    )


def process_contact(name: str, email: str, message: str) -> None:
    """Process contact submission: save to JSON and send email."""
    try:
        email_service.send_contact_email(name, email, message)
        logger.info(f"Contact processed successfully for {name}")
    except Exception as e:
        logger.exception(f"Failed to process contact from {name}: {e}")
        # Don't raise - background task should not fail the response