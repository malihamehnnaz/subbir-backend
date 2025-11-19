"""
Simple data models for the Portfolio Email API.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Annotated


class ContactRequest(BaseModel):
    """Contact form submission data."""
    name: Annotated[str, Field(min_length=2)]
    email: EmailStr
    message: Annotated[str, Field(min_length=10)]


class ContactResponse(BaseModel):
    """Response for contact submissions."""
    status: str
    message: str = "Contact received successfully"