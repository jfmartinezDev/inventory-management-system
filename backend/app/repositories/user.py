"""
User repository for user-specific database operations.
Extends base repository with user-specific queries.
"""

from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.repositories.base import BaseRepository
from app.core.security import get_password_hash, verify_password


class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    """
    Repository for User model operations.
    Handles user-specific database operations.
    """

    def __init__(self):
        """Initialize UserRepository with User model."""
        super().__init__(User)

    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        """
        Get user by email address.

        Args:
            db: Database session
            email: User email

        Returns:
            Optional[User]: User if found, None otherwise
        """
        return db.query(User).filter(User.email == email).first()

    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        """
        Get user by username.

        Args:
            db: Database session
            username: Username

        Returns:
            Optional[User]: User if found, None otherwise
        """
        return db.query(User).filter(User.username == username).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        """
        Create new user with hashed password.

        Args:
            db: Database session
            obj_in: User creation data

        Returns:
            User: Created user
        """
        db_obj = User(
            email=obj_in.email,
            username=obj_in.username,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            is_active=obj_in.is_active,
            is_superuser=obj_in.is_superuser,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: User, obj_in: UserUpdate) -> User:
        """
        Update user with password hashing if password is updated.

        Args:
            db: Database session
            db_obj: Existing user object
            obj_in: Update data

        Returns:
            User: Updated user
        """
        update_data = obj_in.model_dump(exclude_unset=True)

        # Hash password if it's being updated
        if "password" in update_data:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password

        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(
        self, db: Session, *, username: str, password: str
    ) -> Optional[User]:
        """
        Authenticate user with username and password.

        Args:
            db: Database session
            username: Username or email
            password: Plain text password

        Returns:
            Optional[User]: User if authenticated, None otherwise
        """
        # Try to find user by username or email
        user = self.get_by_username(db, username=username)
        if not user:
            user = self.get_by_email(db, email=username)

        if not user:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        return user

    def is_active(self, user: User) -> bool:
        """
        Check if user is active.

        Args:
            user: User object

        Returns:
            bool: True if user is active, False otherwise
        """
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        """
        Check if user is superuser.

        Args:
            user: User object

        Returns:
            bool: True if user is superuser, False otherwise
        """
        return user.is_superuser


# Create singleton instance
user_repository = UserRepository()
