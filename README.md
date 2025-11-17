# Email API (FastAPI)

Minimal FastAPI service to accept contact form POSTs and send email via SMTP.

Files:
- `main.py` - FastAPI app exposing `POST /send`.
- `schemas.py` - Pydantic request model.
- `sender.py` - SMTP sending logic.
- `.env.example` - example environment variables.
- `requirements.txt` - Python dependencies.
- `test_email.py` - pytest unit tests (mocks SMTP).

Quick start (local):

1. Create a virtual environment and activate it.
2. Install dependencies:

```powershell
python -m pip install -r services/email_api/requirements.txt
```

3. Create a `.env` file next to `main.py` (or set environment variables) using `.env.example` as a template.

4. Run the server:

```powershell
uvicorn services.email_api.main:app --reload --port 8000
```

5. POST JSON to `http://localhost:8000/send` with body:

```json
{
  "name": "Alice",
  "email": "alice@example.com",
  "message": "Hello!"
}
```

Notes:
- This implementation uses SMTP credentials (SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD). See `.env.example`.
- For production, use a transactional email provider (SendGrid, Mailgun) or a secure mail relay and set credentials in environment variables.

Docker + MailHog (recommended for local dev)

1. Build and run with docker-compose (requires Docker):

```powershell
cd services/email_api
docker compose up --build
```

2. MailHog web UI: http://localhost:8025 (captures emails sent by the app)
3. Swagger UI: http://localhost:8000/docs

Dry-run mode

If you want to test the API without configuring SMTP, set the environment variable `EMAIL_DRY_RUN=true`.

Local dev helper (PowerShell)

If you're on Windows you can use the included helper script to load `.env.dev` and start the app:

```powershell
# from repo root
.\services\email_api\run-local.ps1
```

Before running the helper you may want to start MailHog (to capture messages) with:

```powershell
cd services/email_api
docker compose up -d mailhog
```

Production notes
- Store SMTP/API keys in a secure store (AWS Secrets Manager, Azure Key Vault, GitHub Secrets, etc.) and never commit them to the repo.
- For high volume, use a transactional provider and a task queue for sending retries.
