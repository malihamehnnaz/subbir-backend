"""
Email service for handling SMTP operations and contact logging.
"""

import json
import smtplib
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path
from typing import Dict, Any

from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from app.core import get_logger, get_settings


logger = get_logger(__name__)


class EmailService:
    """Service for sending emails via SMTP."""
    
    def __init__(self):
        self.settings = get_settings()
    
    @retry(
        reraise=True,
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type(Exception),
    )
    def _send_via_smtp(self, msg: EmailMessage) -> None:
        """Send email message via SMTP with retry logic."""
        host = self.settings.smtp_host
        port = self.settings.smtp_port
        user = self.settings.smtp_user
        password = self.settings.smtp_password
        
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
    
    def _save_contact_to_json(self, name: str, sender_email: str, message_body: str) -> None:
        """Save contact submission to JSON file for record keeping."""
        contact_data = {
            "timestamp": datetime.now().isoformat(),
            "name": name,
            "email": sender_email,
            "message": message_body,
            "status": "received"
        }
        
        # Ensure data directory exists
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        
        # Save to JSON file (one file per day)
        date_str = datetime.now().strftime("%Y-%m-%d")
        json_file = data_dir / f"contacts_{date_str}.json"
        
        # Read existing data or create new list
        contacts = []
        if json_file.exists():
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    contacts = json.load(f)
            except (json.JSONDecodeError, Exception) as e:
                logger.warning(f"Could not read existing contacts file: {e}")
                contacts = []
        
        # Add new contact and save
        contacts.append(contact_data)
        try:
            with open(json_file, "w", encoding="utf-8") as f:
                json.dump(contacts, f, indent=2, ensure_ascii=False)
            logger.info(f"Contact saved to {json_file}")
        except Exception as e:
            logger.error(f"Failed to save contact to JSON: {e}")
    
    def send_contact_email(self, name: str, sender_email: str, message_body: str) -> bool:
        """
        Send a contact form email.
        
        Args:
            name: Name of the person sending the message
            sender_email: Email address of the sender
            message_body: Content of the message
            
        Returns:
            bool: True if email was sent successfully, False otherwise
            
        Raises:
            RuntimeError: If SMTP configuration is incomplete
        """
        # Always save contact to JSON for record keeping
        self._save_contact_to_json(name, sender_email, message_body)
        
        # Check for dry-run mode
        if self.settings.email_dry_run:
            logger.info(
                "Dry-run enabled; not sending email. "
                f"From: {name} <{sender_email}>, Contact saved to JSON."
            )
            return True
        
        # Validate SMTP configuration
        required_settings = [
            self.settings.smtp_host,
            self.settings.smtp_user,
            self.settings.smtp_password,
            self.settings.email_to
        ]
        
        if not all(required_settings):
            raise RuntimeError("Missing SMTP configuration. Check environment variables.")
        
        # Create email message
        msg = EmailMessage()
        msg["From"] = self.settings.email_from
        msg["To"] = self.settings.email_to
        msg["Subject"] = f"New contact form message from {name}"
        
        body = f"Name: {name}\nEmail: {sender_email}\n\nMessage:\n{message_body}\n"
        msg.set_content(body)
        
        try:
            self._send_via_smtp(msg)
            logger.info(f"Email sent successfully for contact from {name}")
            return True
        except Exception as e:
            logger.exception(f"Failed to send email for contact from {name}: {e}")
            raise


# Global email service instance
email_service = EmailService()