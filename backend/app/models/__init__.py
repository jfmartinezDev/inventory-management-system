"""
Models module initialization.
Exports all database models for easy import.
"""

from app.models.base import Base
from app.models.user import User
from app.models.product import Product

__all__ = ["Base", "User", "Product"]
