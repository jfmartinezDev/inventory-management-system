"""
User management endpoints.
Handles user CRUD operations and profile management.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core import database
from app.api.deps import (
    get_current_active_user,
    get_current_active_superuser,
    PaginationParams
)
from app.models.user import User as UserModel
from app.repositories.user import user_repository
from app.schemas.user import User, UserUpdate

router = APIRouter()


@router.get("/me", response_model=User)
async def read_users_me(
    current_user: UserModel = Depends(get_current_active_user)
) -> User:
    """
    Get current user profile.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        User: Current user profile
    """
    return current_user


@router.put("/me", response_model=User)
async def update_user_me(
    *,
    db: Session = Depends(database.get_db),
    user_in: UserUpdate,
    current_user: UserModel = Depends(get_current_active_user)
) -> User:
    """
    Update current user profile.
    
    Args:
        db: Database session
        user_in: User update data
        current_user: Current authenticated user
        
    Returns:
        User: Updated user profile
    """
    # Check if email is being updated and already exists
    if user_in.email and user_in.email != current_user.email:
        existing_user = user_repository.get_by_email(db, email=user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    # Check if username is being updated and already exists
    if user_in.username and user_in.username != current_user.username:
        existing_user = user_repository.get_by_username(db, username=user_in.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
    
    user = user_repository.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get("/", response_model=List[User])
async def read_users(
    db: Session = Depends(database.get_db),
    pagination: PaginationParams = Depends(),
    current_user: UserModel = Depends(get_current_active_superuser)
) -> List[User]:
    """
    Get all users (superuser only).
    
    Args:
        db: Database session
        pagination: Pagination parameters
        current_user: Current superuser
        
    Returns:
        List[User]: List of users
    """
    users = user_repository.get_multi(
        db,
        skip=pagination.skip,
        limit=pagination.limit,
        order_by=pagination.order_by,
        order_direction=pagination.order_direction
    )
    return users


@router.get("/{user_id}", response_model=User)
async def read_user_by_id(
    user_id: int,
    db: Session = Depends(database.get_db),
    current_user: UserModel = Depends(get_current_active_superuser)
) -> User:
    """
    Get a specific user by ID (superuser only).
    
    Args:
        user_id: User ID
        db: Database session
        current_user: Current superuser
        
    Returns:
        User: User profile
        
    Raises:
        HTTPException: If user not found
    """
    user = user_repository.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: Session = Depends(database.get_db),
    current_user: UserModel = Depends(get_current_active_superuser)
) -> None:
    """
    Delete a user (superuser only).
    
    Args:
        user_id: User ID to delete
        db: Database session
        current_user: Current superuser
        
    Raises:
        HTTPException: If user not found or trying to delete self
    """
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete yourself"
        )
    
    user = user_repository.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user_repository.remove(db, id=user_id)