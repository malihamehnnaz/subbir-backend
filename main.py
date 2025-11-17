from fastapi import FastAPI, HTTPException, BackgroundTasks, Request, Response
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

cors_env = os.environ.get("CORS_ALLOW_ORIGIN", "*") or "*"
if isinstance(cors_env, str) and cors_env.strip() == "*":
    allow_origins = ["*"]
else:
    allow_origins = [o.strip() for o in cors_env.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Log startup info so you can verify CORS settings in Railway logs
logger.info(f"Portfolio Email API started. CORS_ALLOW_ORIGIN={cors_env!r} -> allow_origins={allow_origins}")

@app.options("/send")
async def _preflight_send(request: Request) -> Response:
    origin = request.headers.get("origin")
    if allow_origins == ["*"]:
        acao = "*"
    else:
        acao = origin if origin in allow_origins else (allow_origins[0] if allow_origins else "*")

    headers = {
        "Access-Control-Allow-Origin": acao,
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
        "Access-Control-Allow-Credentials": "true",
    }
    return Response(status_code=204, headers=headers)


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
