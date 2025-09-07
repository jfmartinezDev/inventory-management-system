"""
Unit tests for Pydantic schemas.
Tests data validation and serialization without database.
"""

import pytest
from pydantic import ValidationError
from datetime import datetime
from app.schemas.user import UserCreate, UserUpdate, User
from app.schemas.product import ProductCreate, ProductUpdate, Product
from app.schemas.token import Token, TokenData


class TestUserSchemas:
    """Test user-related schemas."""

    def test_user_create_valid(self):
        """Test creating valid user schema."""
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
            "full_name": "Test User",
        }

        user = UserCreate(**user_data)
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.password == "password123"
        assert user.full_name == "Test User"

    def test_user_create_invalid_email(self):
        """Test user creation with invalid email."""
        user_data = {
            "username": "testuser",
            "email": "invalid-email",
            "password": "password123",
        }

        with pytest.raises(ValidationError) as exc_info:
            UserCreate(**user_data)

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("email",) for error in errors)

    def test_user_create_short_username(self):
        """Test user creation with short username."""
        user_data = {
            "username": "ab",  # Too short (min 3)
            "email": "test@example.com",
            "password": "password123",
        }

        with pytest.raises(ValidationError) as exc_info:
            UserCreate(**user_data)

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("username",) for error in errors)

    def test_user_update_partial(self):
        """Test partial user update."""
        update_data = {"email": "newemail@example.com"}

        user_update = UserUpdate(**update_data)
        assert user_update.email == "newemail@example.com"
        assert user_update.username is None
        assert user_update.password is None

    def test_user_response_schema(self):
        """Test user response schema."""
        user_data = {
            "id": 1,
            "username": "testuser",
            "email": "test@example.com",
            "full_name": "Test User",
            "is_active": True,
            "is_superuser": False,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }

        user = User(**user_data)
        assert user.id == 1
        assert user.username == "testuser"
        assert "password" not in user.model_dump()


class TestProductSchemas:
    """Test product-related schemas."""

    def test_product_create_valid(self):
        """Test creating valid product schema."""
        product_data = {
            "name": "Test Product",
            "description": "A test product",
            "sku": "TEST-001",
            "price": 99.99,
            "quantity": 10,
            "min_stock": 5,
            "category": "Electronics",
            "image_url": "https://example.com/image.jpg",
        }

        product = ProductCreate(**product_data)
        assert product.name == "Test Product"
        assert product.price == 99.99
        assert product.quantity == 10

    def test_product_create_negative_price(self):
        """Test product creation with negative price."""
        product_data = {
            "name": "Test Product",
            "sku": "TEST-001",
            "price": -10.00,  # Invalid negative price
            "quantity": 10,
        }

        with pytest.raises(ValidationError) as exc_info:
            ProductCreate(**product_data)

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("price",) for error in errors)

    def test_product_create_negative_quantity(self):
        """Test product creation with negative quantity."""
        product_data = {
            "name": "Test Product",
            "sku": "TEST-001",
            "price": 10.00,
            "quantity": -5,  # Invalid negative quantity
        }

        with pytest.raises(ValidationError) as exc_info:
            ProductCreate(**product_data)

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("quantity",) for error in errors)

    def test_product_price_rounding(self):
        """Test that price is rounded to 2 decimal places."""
        product_data = {
            "name": "Test Product",
            "sku": "TEST-001",
            "price": 10.999,  # Should be rounded to 11.00
            "quantity": 10,
        }

        product = ProductCreate(**product_data)
        assert product.price == 11.00

    def test_product_update_partial(self):
        """Test partial product update."""
        update_data = {"price": 149.99, "quantity": 25}

        product_update = ProductUpdate(**update_data)
        assert product_update.price == 149.99
        assert product_update.quantity == 25
        assert product_update.name is None
        assert product_update.sku is None

    def test_product_empty_sku(self):
        """Test product creation with empty SKU."""
        product_data = {
            "name": "Test Product",
            "sku": "",  # Empty SKU should fail
            "price": 10.00,
            "quantity": 10,
        }

        with pytest.raises(ValidationError) as exc_info:
            ProductCreate(**product_data)

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("sku",) for error in errors)


class TestTokenSchemas:
    """Test token-related schemas."""

    def test_token_schema(self):
        """Test token response schema."""
        token_data = {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "token_type": "bearer",
        }

        token = Token(**token_data)
        assert token.access_token == token_data["access_token"]
        assert token.token_type == "bearer"

    def test_token_data_schema(self):
        """Test token data schema."""
        token_data = TokenData(username="testuser")
        assert token_data.username == "testuser"

        token_data_empty = TokenData()
        assert token_data_empty.username is None
