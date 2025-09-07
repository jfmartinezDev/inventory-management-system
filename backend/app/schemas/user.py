"""
Pydantic schemas for User model.
Handles data validation and serialization.
"""

from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict, Field
from datetime import datetime


class UserBase(BaseModel):
    """Base schema for User with common attributes."""

    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = None
    is_active: bool = True
    is_superuser: bool = False


class UserCreate(UserBase):
    """Schema for creating a new user."""

    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    """Schema for updating an existing user."""

    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    full_name: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8)
    is_active: Optional[bool] = None


class UserInDBBase(UserBase):
    """Base schema for User stored in database."""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class User(UserInDBBase):
    """Schema for User response."""

    pass


class UserInDB(UserInDBBase):
    """Schema for User in database with hashed password."""

    hashed_password: str
