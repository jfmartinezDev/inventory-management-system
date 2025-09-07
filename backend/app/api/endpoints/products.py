"""
Product management endpoints.
Handles product CRUD operations and inventory management.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core import database
from app.api.deps import get_current_active_user, PaginationParams
from app.models.user import User
from app.repositories.product import product_repository
from app.schemas.product import Product, ProductCreate, ProductUpdate, ProductList

router = APIRouter()


@router.get("/", response_model=ProductList)
async def read_products(
    db: Session = Depends(database.get_db),
    pagination: PaginationParams = Depends(),
    search: Optional[str] = Query(None, description="Search query"),
    category: Optional[str] = Query(None, description="Filter by category"),
    low_stock: bool = Query(False, description="Show only low stock items"),
    current_user: User = Depends(get_current_active_user),
) -> ProductList:
    """
    Get all products with optional filtering and search.

    Args:
        db: Database session
        pagination: Pagination parameters
        search: Optional search query
        category: Optional category filter
        low_stock: Show only low stock items
        current_user: Current authenticated user

    Returns:
        ProductList: Paginated list of products
    """
    # Apply filters based on query parameters
    if search:
        products = product_repository.search(
            db, query=search, skip=pagination.skip, limit=pagination.limit
        )
    elif category:
        products = product_repository.get_by_category(
            db, category=category, skip=pagination.skip, limit=pagination.limit
        )
    elif low_stock:
        products = product_repository.get_low_stock(
            db, skip=pagination.skip, limit=pagination.limit
        )
    else:
        products = product_repository.get_multi(
            db,
            skip=pagination.skip,
            limit=pagination.limit,
            order_by=pagination.order_by,
            order_direction=pagination.order_direction,
        )

    # Get total count for pagination
    total = product_repository.count(db)
    pages = (total + pagination.size - 1) // pagination.size

    return ProductList(
        items=products,
        total=total,
        page=pagination.page,
        size=pagination.size,
        pages=pages,
    )


@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(
    *,
    db: Session = Depends(database.get_db),
    product_in: ProductCreate,
    current_user: User = Depends(get_current_active_user)
) -> Product:
    """
    Create a new product.

    Args:
        db: Database session
        product_in: Product creation data
        current_user: Current authenticated user

    Returns:
        Product: Created product

    Raises:
        HTTPException: If SKU already exists
    """
    # Check if SKU already exists
    existing_product = product_repository.get_by_sku(db, sku=product_in.sku)
    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product with this SKU already exists",
        )

    # Create product with current user as owner
    product = product_repository.create(db, obj_in=product_in, user_id=current_user.id)

    return product


@router.get("/categories", response_model=List[str])
async def read_categories(
    db: Session = Depends(database.get_db),
    current_user: User = Depends(get_current_active_user),
) -> List[str]:
    """
    Get all unique product categories.

    Args:
        db: Database session
        current_user: Current authenticated user

    Returns:
        List[str]: List of unique categories
    """
    categories = product_repository.get_categories(db)
    return categories


@router.get("/low-stock", response_model=List[Product])
async def read_low_stock_products(
    db: Session = Depends(database.get_db),
    pagination: PaginationParams = Depends(),
    current_user: User = Depends(get_current_active_user),
) -> List[Product]:
    """
    Get products with low stock levels.

    Args:
        db: Database session
        pagination: Pagination parameters
        current_user: Current authenticated user

    Returns:
        List[Product]: List of low stock products
    """
    products = product_repository.get_low_stock(
        db, skip=pagination.skip, limit=pagination.limit
    )
    return products


@router.get("/inventory-value", response_model=dict)
async def get_inventory_value(
    db: Session = Depends(database.get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    Get total inventory value.

    Args:
        db: Database session
        current_user: Current authenticated user

    Returns:
        dict: Total inventory value and statistics
    """
    total_value = product_repository.get_total_value(db)
    total_products = product_repository.count(db)
    low_stock_count = len(product_repository.get_low_stock(db))

    return {
        "total_value": round(total_value, 2),
        "total_products": total_products,
        "low_stock_count": low_stock_count,
    }


@router.get("/{product_id}", response_model=Product)
async def read_product(
    product_id: int,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(get_current_active_user),
) -> Product:
    """
    Get a specific product by ID.

    Args:
        product_id: Product ID
        db: Database session
        current_user: Current authenticated user

    Returns:
        Product: Product details

    Raises:
        HTTPException: If product not found
    """
    product = product_repository.get(db, id=product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return product


@router.put("/{product_id}", response_model=Product)
async def update_product(
    *,
    product_id: int,
    db: Session = Depends(database.get_db),
    product_in: ProductUpdate,
    current_user: User = Depends(get_current_active_user)
) -> Product:
    """
    Update a product.

    Args:
        product_id: Product ID
        db: Database session
        product_in: Product update data
        current_user: Current authenticated user

    Returns:
        Product: Updated product

    Raises:
        HTTPException: If product not found or SKU already exists
    """
    product = product_repository.get(db, id=product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    # Check if user owns the product or is superuser
    if product.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )

    # Check if SKU is being updated and already exists
    if product_in.sku and product_in.sku != product.sku:
        existing_product = product_repository.get_by_sku(db, sku=product_in.sku)
        if existing_product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product with this SKU already exists",
            )

    product = product_repository.update(db, db_obj=product, obj_in=product_in)
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(get_current_active_user),
) -> None:
    """
    Delete a product.

    Args:
        product_id: Product ID
        db: Database session
        current_user: Current authenticated user

    Raises:
        HTTPException: If product not found or insufficient permissions
    """
    product = product_repository.get(db, id=product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    # Check if user owns the product or is superuser
    if product.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )

    product_repository.remove(db, id=product_id)


@router.patch("/{product_id}/stock", response_model=Product)
async def update_product_stock(
    product_id: int,
    quantity_change: int = Query(
        ..., description="Quantity to add (positive) or subtract (negative)"
    ),
    db: Session = Depends(database.get_db),
    current_user: User = Depends(get_current_active_user),
) -> Product:
    """
    Update product stock quantity.

    Args:
        product_id: Product ID
        quantity_change: Quantity change (positive to add, negative to subtract)
        db: Database session
        current_user: Current authenticated user

    Returns:
        Product: Updated product

    Raises:
        HTTPException: If product not found
    """
    product = product_repository.update_stock(
        db, product_id=product_id, quantity_change=quantity_change
    )

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    return product
