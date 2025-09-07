"""
Pydantic schemas for Product model.
Handles data validation and serialization.
"""

from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import datetime


class ProductBase(BaseModel):
    """Base schema for Product with common attributes."""

    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    sku: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)
    quantity: int = Field(..., ge=0)
    image_url: Optional[str] = None
    category: Optional[str] = None
    min_stock: int = Field(default=0, ge=0)

    @field_validator("price")
    @classmethod
    def validate_price(cls, v):
        """Ensure price has maximum 2 decimal places."""
        return round(v, 2)


class ProductCreate(ProductBase):
    """Schema for creating a new product."""

    pass


class ProductUpdate(BaseModel):
    """Schema for updating an existing product."""

    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    sku: Optional[str] = Field(None, min_length=1, max_length=100)
    price: Optional[float] = Field(None, gt=0)
    quantity: Optional[int] = Field(None, ge=0)
    image_url: Optional[str] = None
    category: Optional[str] = None
    min_stock: Optional[int] = Field(None, ge=0)

    @field_validator("price")
    @classmethod
    def validate_price(cls, v):
        """Ensure price has maximum 2 decimal places."""
        if v is not None:
            return round(v, 2)
        return v


class ProductInDBBase(ProductBase):
    """Base schema for Product stored in database."""

    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    is_low_stock: bool
    total_value: float

    model_config = ConfigDict(from_attributes=True)


class Product(ProductInDBBase):
    """Schema for Product response."""

    pass


class ProductList(BaseModel):
    """Schema for paginated product list response."""

    items: list[Product]
    total: int
    page: int
    size: int
    pages: int
