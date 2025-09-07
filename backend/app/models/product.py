"""
Product model for inventory management.
Represents products in the inventory system.
"""

from sqlalchemy import Column, String, Float, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.models.base import Base


class Product(Base):
    """
    Product model representing inventory items.
    Stores product details and relationships.
    """
    
    __tablename__ = "products"
    
    # Product details
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    sku = Column(String, unique=True, index=True, nullable=False)
    
    # Pricing and quantity
    price = Column(Float, nullable=False)
    quantity = Column(Integer, default=0, nullable=False)
    
    # Additional fields for optional enhancements
    image_url = Column(String, nullable=True)
    category = Column(String, nullable=True, index=True)
    min_stock = Column(Integer, default=0)
    
    # Relationships
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_by = relationship("User", back_populates="products")
    
    def __repr__(self):
        """String representation of Product."""
        return f"<Product(id={self.id}, name='{self.name}', sku='{self.sku}', quantity={self.quantity})>"
    
    @property
    def is_low_stock(self) -> bool:
        """Check if product is below minimum stock level."""
        return self.quantity <= self.min_stock
    
    @property
    def total_value(self) -> float:
        """Calculate total value of product in inventory."""
        return self.price * self.quantity