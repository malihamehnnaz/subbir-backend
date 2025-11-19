# Portfolio Email API

A FastAPI-based email service for portfolio contact forms with background email processing and CORS support.

## Features

- **Simple FastAPI** application for contact forms
- **JSON logging** - All contacts saved to daily JSON files in `/data` directory
- **Email sending** via SMTP (optional, controlled by `EMAIL_DRY_RUN`)
- **CORS support** for frontend integration
- **Clean modular architecture** - Easy to understand and maintain
- **Docker ready** for deployment
- **Background processing** - Non-blocking contact handling
- **Production optimized** - Runs Uvicorn directly with proper settings

## Quick Start

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your SMTP credentials
   ```

3. **Run the API:**
   ```bash
   python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
   ```

### Docker Deployment

**Development (with auto-reload):**
```bash
docker compose up --build
```

**Production:**
```bash
docker compose -f docker-compose.prod.yml up --build -d
```

**Direct Docker Run:**
```bash
docker build -t portfolio-backend .
docker run -p 8000:8000 --env-file .env portfolio-backend
```

## API Endpoints

### `GET /`
Health check endpoint.

**Response:**
```json
{"status": "ready"}
```

### `POST /send`
Send a contact form email.

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com", 
  "message": "Hello, this is a test message that is long enough."
}
```

**Response:**
```json
{
  "status": "accepted", 
  "message": "Your message has been received and will be processed shortly."
}
```

**What happens:**
1. Contact data is immediately saved to JSON file in `/data` directory
2. Email is sent in background (if `EMAIL_DRY_RUN` is not `true`)
3. Both success and failure are logged

**Validation:**
- `name`: minimum 2 characters
- `email`: valid email format  
- `message`: minimum 10 characters

**JSON Files:**
- Contacts are saved to `data/contacts_YYYY-MM-DD.json`
- Each file contains an array of contact submissions for that day
- Files are created automatically and won't be committed to git

## Configuration

Set these environment variables (or use `.env` file):

| Variable | Description | Example |
|----------|-------------|---------|
| `CORS_ALLOW_ORIGIN` | Comma-separated origins or "*" | `https://mysite.com,https://www.mysite.com` |
| `SMTP_HOST` | SMTP server hostname | `smtp.gmail.com` |
| `SMTP_PORT` | SMTP server port | `587` |
| `SMTP_USER` | SMTP username | `your-email@gmail.com` |
| `SMTP_PASSWORD` | SMTP password/app password | `your-app-password` |
| `EMAIL_FROM` | Sender email address | `your-email@gmail.com` |
| `EMAIL_TO` | Recipient email address | `recipient@example.com` |
| `EMAIL_DRY_RUN` | Enable dry-run mode (optional) | `true` |

## Deployment Options

### Railway
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

### Render
1. Connect your GitHub repo to Render
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `python -m uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Configure environment variables

### Docker Hub + Any Server
```bash
# Build and push
docker build -t your-username/portfolio-backend .
docker push your-username/portfolio-backend

# Deploy anywhere
docker run -d -p 8000:8000 --env-file .env your-username/portfolio-backend
```

### Local Docker
```bash
docker compose -f docker-compose.prod.yml up -d
```

## File Structure

```
Portfolio-Backend/
├── app/                      # Main application package
│   ├── __init__.py          # Package initialization  
│   ├── main.py              # FastAPI application
│   ├── api/                 # API routes
│   │   ├── __init__.py
│   │   └── routes.py        # Contact endpoint
│   ├── core/                # Core utilities
│   │   ├── __init__.py
│   │   ├── config.py        # Settings
│   │   └── logging.py       # Logging setup
│   ├── models/              # Data models
│   │   └── __init__.py      # Pydantic models
│   └── services/            # Business logic
│       ├── __init__.py
│       └── email.py         # Email & JSON logging
├── data/                    # JSON contact files
│   └── .gitignore           # Ignore contact data
├── main.py                  # Application entry point
├── requirements.txt         # Dependencies
├── Dockerfile               # Docker config
├── docker-compose.prod.yml  # Production Docker
├── .dockerignore           # Docker exclusions
├── .env.example            # Environment template
└── README.md               # This documentation
```

## Development

### Testing with MailHog

For local testing without sending real emails:

```bash
docker compose --profile dev up
```

Then set in your `.env`:
```
SMTP_HOST=localhost
SMTP_PORT=1025
```

View emails at: http://localhost:8025

### Dry-run Mode

Set `EMAIL_DRY_RUN=true` in `.env` to log emails without sending them.

## Architecture

The application follows a **modular architecture** with clear separation of concerns:

### Core Components
- **FastAPI** provides the async web framework
- **Modular structure** with separate packages for API, core, models, and services
- **Configuration management** with environment-based settings
- **Dependency injection** pattern for services
- **Background tasks** handle email sending without blocking responses

### Key Patterns
- **Application Factory Pattern**: `create_app()` function for flexible app creation
- **Service Layer Pattern**: Business logic isolated in service classes
- **Configuration Pattern**: Centralized settings management
- **Repository Pattern**: Clear data access abstraction

### Technology Stack
- **FastAPI** - Modern, fast web framework with automatic API documentation
- **Pydantic v2** - Data validation and serialization with type hints
- **Tenacity** - Retry logic for reliable email delivery
- **CORS middleware** - Cross-origin request handling for frontend integration
- **Structured logging** - Comprehensive logging with proper formatters

## Security Notes

- Never commit `.env` files to version control
- Use app passwords for Gmail (not your account password)
- Set specific CORS origins in production (not "*")
- Use HTTPS in production environments
- Keep your SMTP credentials secure