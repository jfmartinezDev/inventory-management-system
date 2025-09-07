"""
Test configuration and fixtures for pytest.
Provides common test setup and utilities.
"""

import pytest
from typing import Generator, Dict
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.database import get_db
from app.main import app
from app.models.base import Base
from app.repositories.user import user_repository
from app.schemas.user import UserCreate
from app.core.security import create_access_token

# Use SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Create test engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create test session factory
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db() -> Generator[Session, None, None]:
    """
    Create a fresh database for each test.

    Yields:
        Session: Test database session
    """
    # Create tables
    Base.metadata.create_all(bind=engine)

    # Create session
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        # Drop all tables after test
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db: Session) -> Generator[TestClient, None, None]:
    """
    Create a test client with overridden database dependency.

    Args:
        db: Test database session

    Yields:
        TestClient: FastAPI test client
    """

    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db: Session) -> Dict:
    """
    Create a test user.

    Args:
        db: Database session

    Returns:
        Dict: User data with credentials
    """
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        password="testpassword123",
        full_name="Test User",
        is_active=True,
        is_superuser=False,
    )

    user = user_repository.create(db, obj_in=user_data)

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "password": "testpassword123",
        "full_name": user.full_name,
    }


@pytest.fixture
def test_superuser(db: Session) -> Dict:
    """
    Create a test superuser.

    Args:
        db: Database session

    Returns:
        Dict: Superuser data with credentials
    """
    user_data = UserCreate(
        username="admin",
        email="admin@example.com",
        password="adminpassword123",
        full_name="Admin User",
        is_active=True,
        is_superuser=True,
    )

    user = user_repository.create(db, obj_in=user_data)

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "password": "adminpassword123",
        "full_name": user.full_name,
    }


@pytest.fixture
def auth_headers(test_user: Dict) -> Dict[str, str]:
    """
    Create authentication headers for test user.

    Args:
        test_user: Test user data

    Returns:
        Dict: Authorization headers
    """
    token = create_access_token(subject=test_user["username"])
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def superuser_headers(test_superuser: Dict) -> Dict[str, str]:
    """
    Create authentication headers for test superuser.

    Args:
        test_superuser: Test superuser data

    Returns:
        Dict: Authorization headers
    """
    token = create_access_token(subject=test_superuser["username"])
    return {"Authorization": f"Bearer {token}"}
