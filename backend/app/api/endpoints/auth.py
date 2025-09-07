"""
Authentication endpoints for user login and registration.
Handles user authentication and token generation.
"""

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core import database, security
from app.core.config import settings
from app.repositories.user import user_repository
from app.schemas.token import Token
from app.schemas.user import User, UserCreate

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(
    db: Session = Depends(database.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Token:
    """
    OAuth2 compatible token login endpoint.
    
    Args:
        db: Database session
        form_data: OAuth2 form with username and password
        
    Returns:
        Token: Access token for authentication
        
    Raises:
        HTTPException: If authentication fails
    """
    # Authenticate user
    user = user_repository.authenticate(
        db,
        username=form_data.username,
        password=form_data.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        subject=user.username,
        expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="bearer")


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register(
    *,
    db: Session = Depends(database.get_db),
    user_in: UserCreate
) -> User:
    """
    Register a new user.
    
    Args:
        db: Database session
        user_in: User registration data
        
    Returns:
        User: Created user
        
    Raises:
        HTTPException: If username or email already exists
    """
    # Check if username already exists
    user = user_repository.get_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email already exists
    user = user_repository.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    user = user_repository.create(db, obj_in=user_in)
    
    return user
