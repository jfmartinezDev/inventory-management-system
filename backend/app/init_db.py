"""
Database initialization script.
Creates tables and optionally seeds initial data.
"""

from sqlalchemy.orm import Session
from app.core.database import engine
from app.models.base import Base
from app.models import User, Product  # Import all models
from app.repositories.user import user_repository
from app.schemas.user import UserCreate
from app.core.config import settings


def init_db() -> None:
    """
    Initialize database by creating all tables.
    """
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


def create_superuser(db: Session) -> None:
    """
    Create initial superuser if it doesn't exist.
    
    Args:
        db: Database session
    """
    # Check if superuser already exists
    superuser = user_repository.get_by_username(db, username="admin")
    if not superuser:
        print("Creating superuser...")
        superuser_in = UserCreate(
            username="admin",
            email="admin@inventory.com",
            password="admin123456",  # Change this in production!
            full_name="System Administrator",
            is_active=True,
            is_superuser=True
        )
        user_repository.create(db, obj_in=superuser_in)
        print("Superuser created successfully!")
        print("Username: admin")
        print("Password: admin123456")
        print("Please change the password after first login!")
    else:
        print("Superuser already exists.")


if __name__ == "__main__":
    """
    Run this script to initialize the database.
    """
    from app.core.database import SessionLocal
    
    # Initialize database tables
    init_db()
    
    # Create initial superuser
    db = SessionLocal()
    try:
        create_superuser(db)
    finally:
        db.close()
    
    print("\nDatabase initialization completed!")