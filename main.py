from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
from dotenv import load_dotenv

from .schemas import ContactRequest
from .sender import send_email

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Portfolio Email API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.environ.get("CORS_ALLOW_ORIGIN", "*")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ready"}


def _background_send(name: str, email: str, message: str):
    try:
        send_email(name, email, message)
        logger.info("Email sent in background")
    except Exception as e:
        # Log exception; in production you'd want to notify/alert or push to a retry queue
        logger.exception("Background email send failed: %s", e)


@app.post("/send", status_code=202)
def send_contact(payload: ContactRequest, background_tasks: BackgroundTasks):
    """Accept contact requests and schedule sending in the background.

    Returns 202 Accepted immediately; actual sending runs in background.
    """
    # Optionally support a dry-run mode for local testing when SMTP isn't configured
    dry_run = os.environ.get("EMAIL_DRY_RUN", "false").lower() in ("1", "true", "yes")

    if dry_run:
        logger.info("Dry-run enabled; not sending email. Payload: %s", payload.json())
        return {"status": "accepted", "dry_run": True}

    # schedule background send
    background_tasks.add_task(_background_send, payload.name, payload.email, payload.message)
    return {"status": "accepted"}
