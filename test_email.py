import os
import json
from fastapi.testclient import TestClient

import smtplib

from services.email_api.main import app


class DummySMTP:
    def __init__(self, host=None, port=None):
        self.host = host
        self.port = port
        self.logged_in = False
        self.sent = []

    def ehlo(self):
        return

    def starttls(self):
        return

    def login(self, user, password):
        self.logged_in = True

    def send_message(self, msg):
        # store minimal data so assertions can inspect
        self.sent.append({
            "from": msg["From"],
            "to": msg["To"],
            "subject": msg["Subject"],
            "body": msg.get_content(),
        })

    def quit(self):
        return

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def test_send_contact(monkeypatch, tmp_path):
    # Set env variables
    os.environ["SMTP_HOST"] = "smtp.gmail.com"
    os.environ["SMTP_PORT"] = "587"
    os.environ["SMTP_USER"] = "malihamehnazcse@gmail.com"
    os.environ["SMTP_PASSWORD"] = "pass"
    os.environ["EMAIL_TO"] = "malihamehnazcse@gmail.com"

    dummy = DummySMTP()

    def fake_smtp(host, port):
        return dummy

    monkeypatch.setattr(smtplib, "SMTP", fake_smtp)

    client = TestClient(app)

    payload = {"name": "Test User", "email": "test@example.com", "message": "Hello from test suite!"}
    r = client.post("/send", json=payload)
    # API schedules the send in background and returns 202 Accepted
    assert r.status_code == 202
    data = r.json()
    assert data.get("status") == "accepted"

    # Ensure dummy recorded the message
    assert len(dummy.sent) == 1
    sent = dummy.sent[0]
    assert "Test User" in sent["subject"]
    assert "Hello from test suite" in sent["body"]
