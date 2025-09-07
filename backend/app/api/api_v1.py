"""
Main API router that combines all endpoint routers.
Configures the API v1 routes structure.
"""

from fastapi import APIRouter
from app.api.endpoints import auth, users, products

# Create main API router
api_router = APIRouter()

# Include authentication routes
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"]
)

# Include user management routes
api_router.include_router(
    users.router,
    prefix="/users",
    tags=["Users"]
)

# Include product management routes
api_router.include_router(
    products.router,
    prefix="/products",
    tags=["Products"]
)