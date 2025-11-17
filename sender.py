import os
import logging
from email.message import EmailMessage
import smtplib
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

logger = logging.getLogger(__name__)


def _get_env(var: str, default=None):
    return os.environ.get(var, default)


@retry(
    reraise=True,
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    retry=retry_if_exception_type(Exception),
)
def _send_via_smtp(msg: EmailMessage, host: str, port: int, user: str, password: str) -> None:
    """Low-level SMTP send with retries handled by tenacity decorator."""
    # Use SSL if port is 465, otherwise use STARTTLS
    if port == 465:
        with smtplib.SMTP_SSL(host, port) as server:
            server.login(user, password)
            server.send_message(msg)
    else:
        with smtplib.SMTP(host, port) as server:
            server.ehlo()
            server.starttls()
            server.login(user, password)
            server.send_message(msg)


def send_email(name: str, sender_email: str, message_body: str) -> None:
    """Send an email via SMTP using environment-configured credentials.

    Required env vars (or set in .env for local dev):
    - SMTP_HOST
    - SMTP_PORT
    - SMTP_USER
    - SMTP_PASSWORD
    - EMAIL_FROM (optional, defaults to SMTP_USER)
    - EMAIL_TO (recipient address; default: malihamehnazcse@gmail.com)
    """

    host = _get_env("SMTP_HOST")
    port = int(_get_env("SMTP_PORT", "587"))
    user = _get_env("SMTP_USER")
    password = _get_env("SMTP_PASSWORD")
    email_from = _get_env("EMAIL_FROM", user)
    # default recipient (site owner)
    email_to = _get_env("EMAIL_TO", "malihamehnazcse@gmail.com")

    if not all([host, port, user, password, email_to]):
        raise RuntimeError("Missing SMTP configuration. Check environment variables.")

    msg = EmailMessage()
    msg["From"] = email_from
    msg["To"] = email_to
    msg["Subject"] = f"New contact form message from {name}"
    body = f"Name: {name}\nEmail: {sender_email}\n\nMessage:\n{message_body}\n"
    msg.set_content(body)

    try:
        _send_via_smtp(msg, host, port, user, password)
    except Exception:
        logger.exception("Failed to send email after retries")
        raise
