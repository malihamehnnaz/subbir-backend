"""
Portfolio Email API - Simple contact form handler with JSON logging.

Features:
- Accepts contact form submissions
- Saves all contacts to daily JSON files in /data directory  
- Optionally sends emails via SMTP (based on EMAIL_DRY_RUN setting)
- CORS enabled for frontend integration
"""

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the app
from app.main import app

# Export for uvicorn
__all__ = ["app"]
