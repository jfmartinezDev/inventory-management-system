"""
Base model configuration for SQLAlchemy ORM.
Provides common columns and functionality for all models.
"""

from datetime import datetime
from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from typing import Any


@as_declarative()
class Base:
    """
    Base class for all SQLAlchemy models.
    Provides common attributes and configuration.
    """
    
    # Generate __tablename__ automatically from class name
    @declared_attr
    def __tablename__(cls) -> str:
        """Generate table name from class name in snake_case."""
        return cls.__name__.lower()
    
    # Common columns for all models
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Make SQLAlchemy models JSON serializable
    def dict(self) -> dict:
        """Convert model to dictionary."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}