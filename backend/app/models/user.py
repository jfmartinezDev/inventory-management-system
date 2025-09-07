"""
User model for authentication and authorization.
Handles user data persistence and relationships.
"""

from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship
from app.models.base import Base


class User(Base):
    """
    User model representing system users.
    Stores authentication credentials and profile information.
    """

    __tablename__ = "users"

    # User credentials
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # User profile
    full_name = Column(String, nullable=True)

    # User status
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    # Relationships
    products = relationship(
        "Product", back_populates="created_by", cascade="all, delete-orphan"
    )

    def __repr__(self):
        """String representation of User."""
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
