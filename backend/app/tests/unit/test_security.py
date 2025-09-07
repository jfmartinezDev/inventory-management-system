"""
Unit tests for security utilities.
Tests password hashing and JWT token functions without database.
"""

import pytest
from datetime import timedelta
from jose import jwt
from app.core.security import (
    create_access_token,
    verify_token,
    verify_password,
    get_password_hash
)
from app.core.config import settings


class TestPasswordHashing:
    """Test password hashing functions."""
    
    def test_get_password_hash(self):
        """Test password hashing."""
        password = "testpassword123"
        hashed = get_password_hash(password)
        
        assert hashed != password
        assert len(hashed) > 20
        assert hashed.startswith("$2b$")
    
    def test_verify_password_correct(self):
        """Test verifying correct password."""
        password = "testpassword123"
        hashed = get_password_hash(password)
        
        assert verify_password(password, hashed) is True
    
    def test_verify_password_incorrect(self):
        """Test verifying incorrect password."""
        password = "testpassword123"
        wrong_password = "wrongpassword"
        hashed = get_password_hash(password)
        
        assert verify_password(wrong_password, hashed) is False
    
    def test_same_password_different_hash(self):
        """Test that same password generates different hashes."""
        password = "testpassword123"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        
        assert hash1 != hash2
        assert verify_password(password, hash1) is True
        assert verify_password(password, hash2) is True


class TestJWTTokens:
    """Test JWT token functions."""
    
    def test_create_access_token(self):
        """Test creating access token."""
        subject = "testuser"
        token = create_access_token(subject)
        
        assert token is not None
        assert len(token) > 20
        assert "." in token  # JWT format check
    
    def test_create_access_token_with_expiry(self):
        """Test creating token with custom expiry."""
        subject = "testuser"
        expires_delta = timedelta(minutes=15)
        token = create_access_token(subject, expires_delta)
        
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        
        assert payload["sub"] == subject
        assert "exp" in payload
        assert payload["type"] == "access"
    
    def test_verify_valid_token(self):
        """Test verifying valid token."""
        subject = "testuser"
        token = create_access_token(subject)
        
        decoded_subject = verify_token(token)
        assert decoded_subject == subject
    
    def test_verify_invalid_token(self):
        """Test verifying invalid token."""
        invalid_token = "invalid.token.here"
        
        decoded = verify_token(invalid_token)
        assert decoded is None
    
    def test_verify_expired_token(self):
        """Test verifying expired token."""
        subject = "testuser"
        # Create token that expires immediately
        token = create_access_token(subject, timedelta(seconds=-1))
        
        decoded = verify_token(token)
        assert decoded is None
    
    def test_token_payload_structure(self):
        """Test token payload has correct structure."""
        subject = "testuser"
        token = create_access_token(subject)
        
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        
        assert "sub" in payload
        assert "exp" in payload
        assert "type" in payload
        assert payload["sub"] == subject
        assert payload["type"] == "access"