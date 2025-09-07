"""
Pydantic schemas for authentication tokens.
Handles JWT token data structures.
"""

from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    """Schema for authentication token response."""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for token payload data."""

    username: Optional[str] = None
