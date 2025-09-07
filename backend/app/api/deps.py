"""
API dependencies for authentication and authorization.
Provides reusable dependencies for API endpoints.
"""

from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.core import config, database
from app.core.config import settings
from app.models.user import User
from app.repositories.user import user_repository
from app.schemas.token import TokenData

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


def get_db() -> Session:
    """
    Dependency to get database session.

    Yields:
        Session: Database session
    """
    return next(database.get_db())


async def get_current_user(
    db: Session = Depends(database.get_db), token: str = Depends(oauth2_scheme)
) -> User:
    """
    Get current authenticated user from JWT token.

    Args:
        db: Database session
        token: JWT access token

    Returns:
        User: Current authenticated user

    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = user_repository.get_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Get current active user.

    Args:
        current_user: Current authenticated user

    Returns:
        User: Current active user

    Raises:
        HTTPException: If user is inactive
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return current_user


async def get_current_active_superuser(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """
    Get current active superuser.

    Args:
        current_user: Current active user

    Returns:
        User: Current superuser

    Raises:
        HTTPException: If user is not superuser
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )
    return current_user


class PaginationParams:
    """
    Pagination parameters for list endpoints.
    """

    def __init__(
        self,
        page: int = 1,
        size: int = 50,
        order_by: Optional[str] = None,
        order_direction: str = "asc",
    ):
        """
        Initialize pagination parameters.

        Args:
            page: Page number (1-indexed)
            size: Page size
            order_by: Field to order by
            order_direction: Order direction ('asc' or 'desc')
        """
        self.page = max(1, page)
        self.size = min(100, max(1, size))
        self.skip = (self.page - 1) * self.size
        self.limit = self.size
        self.order_by = order_by
        self.order_direction = order_direction
