"""
Product repository for product-specific database operations.
Extends base repository with product-specific queries.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate
from app.repositories.base import BaseRepository


class ProductRepository(BaseRepository[Product, ProductCreate, ProductUpdate]):
    """
    Repository for Product model operations.
    Handles product-specific database operations.
    """

    def __init__(self):
        """Initialize ProductRepository with Product model."""
        super().__init__(Product)

    def get_by_sku(self, db: Session, *, sku: str) -> Optional[Product]:
        """
        Get product by SKU.

        Args:
            db: Database session
            sku: Product SKU

        Returns:
            Optional[Product]: Product if found, None otherwise
        """
        return db.query(Product).filter(Product.sku == sku).first()

    def get_by_user(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Product]:
        """
        Get products created by a specific user.

        Args:
            db: Database session
            user_id: User ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List[Product]: List of user's products
        """
        return (
            db.query(Product)
            .filter(Product.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def search(
        self, db: Session, *, query: str, skip: int = 0, limit: int = 100
    ) -> List[Product]:
        """
        Search products by name, description, or SKU.

        Args:
            db: Database session
            query: Search query string
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List[Product]: List of matching products
        """
        search_filter = or_(
            Product.name.ilike(f"%{query}%"),
            Product.description.ilike(f"%{query}%"),
            Product.sku.ilike(f"%{query}%"),
        )

        return db.query(Product).filter(search_filter).offset(skip).limit(limit).all()

    def get_by_category(
        self, db: Session, *, category: str, skip: int = 0, limit: int = 100
    ) -> List[Product]:
        """
        Get products by category.

        Args:
            db: Database session
            category: Product category
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List[Product]: List of products in category
        """
        return (
            db.query(Product)
            .filter(Product.category == category)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_low_stock(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Product]:
        """
        Get products with low stock (quantity <= min_stock).

        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List[Product]: List of low stock products
        """
        return (
            db.query(Product)
            .filter(Product.quantity <= Product.min_stock)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_categories(self, db: Session) -> List[str]:
        """
        Get all unique product categories.

        Args:
            db: Database session

        Returns:
            List[str]: List of unique categories
        """
        categories = (
            db.query(Product.category)
            .filter(Product.category.isnot(None))
            .distinct()
            .all()
        )
        return [cat[0] for cat in categories]

    def update_stock(
        self, db: Session, *, product_id: int, quantity_change: int
    ) -> Optional[Product]:
        """
        Update product stock quantity.

        Args:
            db: Database session
            product_id: Product ID
            quantity_change: Quantity to add (positive) or subtract (negative)

        Returns:
            Optional[Product]: Updated product if found, None otherwise
        """
        product = self.get(db, id=product_id)
        if product:
            new_quantity = product.quantity + quantity_change
            if new_quantity < 0:
                new_quantity = 0

            product.quantity = new_quantity
            db.add(product)
            db.commit()
            db.refresh(product)

        return product

    def get_total_value(self, db: Session, *, user_id: Optional[int] = None) -> float:
        """
        Calculate total inventory value.

        Args:
            db: Database session
            user_id: Optional user ID to filter by

        Returns:
            float: Total inventory value
        """
        query = db.query(Product)
        if user_id:
            query = query.filter(Product.user_id == user_id)

        products = query.all()
        return sum(p.total_value for p in products)


# Create singleton instance
product_repository = ProductRepository()
