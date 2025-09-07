"""
Main FastAPI application configuration.
Sets up the API server with middleware, routes, and documentation.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.api_v1 import api_router
from app.core.config import settings

# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Full-stack inventory management system with secure authentication and CRUD operations",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(
    api_router,
    prefix=settings.API_V1_STR
)

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint returning API information.
    
    Returns:
        dict: API information
    """
    return {
        "name": settings.PROJECT_NAME,
        "version": "1.0.0",
        "description": "Inventory Management System API",
        "documentation": "/docs",
        "health": "ok"
    }

# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint for monitoring.
    
    Returns:
        dict: Health status
    """
    return {
        "status": "healthy",
        "service": "inventory-api",
        "environment": settings.ENVIRONMENT
    }