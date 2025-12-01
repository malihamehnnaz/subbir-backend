"""
Middleware for request logging and error handling.
"""
import time
from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.core import get_logger
from app.core.exceptions import EmailServiceError, EmailConfigurationError

logger = get_logger(__name__)


async def log_requests_middleware(request: Request, call_next):
    """Log all incoming requests and their processing time."""
    start_time = time.time()
    
    # Log request
    logger.info(f"{request.method} {request.url.path}")
    
    # Process request
    response = await call_next(request)
    
    # Calculate processing time
    process_time = time.time() - start_time
    
    # Log response
    logger.info(
        f"{request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Time: {process_time:.3f}s"
    )
    
    return response


async def error_handler_middleware(request: Request, call_next):
    """Handle errors globally."""
    try:
        return await call_next(request)
    except EmailConfigurationError as e:
        logger.error(f"Configuration error: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "error": "Service configuration error",
                "message": "Email service is not properly configured"
            }
        )
    except EmailServiceError as e:
        logger.error(f"Email service error: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "Email service error",
                "message": "Failed to process email request"
            }
        )
    except Exception as e:
        logger.exception(f"Unexpected error: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "Internal server error",
                "message": "An unexpected error occurred"
            }
        )
