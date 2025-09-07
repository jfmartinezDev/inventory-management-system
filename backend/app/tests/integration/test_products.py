"""
Integration tests for product endpoints.
Tests the complete flow with database interaction.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.core.config import settings


class TestProductEndpoints:
    """Test product CRUD endpoints."""

    def test_create_product(self, client: TestClient, db: Session, auth_headers):
        """Test creating a new product."""
        product_data = {
            "name": "Test Product",
            "description": "A test product description",
            "sku": "TEST-001",
            "price": 99.99,
            "quantity": 10,
            "min_stock": 5,
            "category": "Electronics",
            "image_url": "https://example.com/image.jpg",
        }

        response = client.post(
            f"{settings.API_V1_STR}/products/", json=product_data, headers=auth_headers
        )

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == product_data["name"]
        assert data["sku"] == product_data["sku"]
        assert data["price"] == product_data["price"]
        assert "id" in data

    def test_create_product_duplicate_sku(
        self, client: TestClient, db: Session, auth_headers
    ):
        """Test creating product with duplicate SKU."""
        product_data = {
            "name": "Product 1",
            "sku": "DUP-001",
            "price": 50.00,
            "quantity": 5,
        }

        # Create first product
        response = client.post(
            f"{settings.API_V1_STR}/products/", json=product_data, headers=auth_headers
        )
        assert response.status_code == 201

        # Try to create second product with same SKU
        product_data["name"] = "Product 2"
        response = client.post(
            f"{settings.API_V1_STR}/products/", json=product_data, headers=auth_headers
        )
        assert response.status_code == 400
        assert "SKU already exists" in response.json()["detail"]

    def test_get_products_list(self, client: TestClient, db: Session, auth_headers):
        """Test getting products list."""
        # Create test products
        for i in range(3):
            product_data = {
                "name": f"Product {i}",
                "sku": f"PROD-{i:03d}",
                "price": 10.00 * (i + 1),
                "quantity": 5 * (i + 1),
            }
            client.post(
                f"{settings.API_V1_STR}/products/",
                json=product_data,
                headers=auth_headers,
            )

        # Get products list
        response = client.get(f"{settings.API_V1_STR}/products/", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert data["total"] >= 3
        assert len(data["items"]) >= 3

    def test_get_product_by_id(self, client: TestClient, db: Session, auth_headers):
        """Test getting product by ID."""
        # Create product
        product_data = {
            "name": "Test Product",
            "sku": "GET-001",
            "price": 99.99,
            "quantity": 10,
        }

        create_response = client.post(
            f"{settings.API_V1_STR}/products/", json=product_data, headers=auth_headers
        )
        product_id = create_response.json()["id"]

        # Get product by ID
        response = client.get(
            f"{settings.API_V1_STR}/products/{product_id}", headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == product_id
        assert data["name"] == product_data["name"]

    def test_get_nonexistent_product(
        self, client: TestClient, db: Session, auth_headers
    ):
        """Test getting non-existent product."""
        response = client.get(
            f"{settings.API_V1_STR}/products/99999", headers=auth_headers
        )

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_update_product(self, client: TestClient, db: Session, auth_headers):
        """Test updating a product."""
        # Create product
        product_data = {
            "name": "Original Product",
            "sku": "UPD-001",
            "price": 50.00,
            "quantity": 10,
        }

        create_response = client.post(
            f"{settings.API_V1_STR}/products/", json=product_data, headers=auth_headers
        )
        product_id = create_response.json()["id"]

        # Update product
        update_data = {"name": "Updated Product", "price": 75.00, "quantity": 20}

        response = client.put(
            f"{settings.API_V1_STR}/products/{product_id}",
            json=update_data,
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == update_data["name"]
        assert data["price"] == update_data["price"]
        assert data["quantity"] == update_data["quantity"]
        assert data["sku"] == product_data["sku"]  # SKU unchanged

    def test_delete_product(self, client: TestClient, db: Session, auth_headers):
        """Test deleting a product."""
        # Create product
        product_data = {
            "name": "To Delete",
            "sku": "DEL-001",
            "price": 25.00,
            "quantity": 5,
        }

        create_response = client.post(
            f"{settings.API_V1_STR}/products/", json=product_data, headers=auth_headers
        )
        product_id = create_response.json()["id"]

        # Delete product
        response = client.delete(
            f"{settings.API_V1_STR}/products/{product_id}", headers=auth_headers
        )

        assert response.status_code == 204

        # Verify product is deleted
        get_response = client.get(
            f"{settings.API_V1_STR}/products/{product_id}", headers=auth_headers
        )
        assert get_response.status_code == 404

    def test_update_stock(self, client: TestClient, db: Session, auth_headers):
        """Test updating product stock."""
        # Create product
        product_data = {
            "name": "Stock Test",
            "sku": "STK-001",
            "price": 30.00,
            "quantity": 10,
        }

        create_response = client.post(
            f"{settings.API_V1_STR}/products/", json=product_data, headers=auth_headers
        )
        product_id = create_response.json()["id"]

        # Add stock
        response = client.patch(
            f"{settings.API_V1_STR}/products/{product_id}/stock?quantity_change=5",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["quantity"] == 15

        # Remove stock
        response = client.patch(
            f"{settings.API_V1_STR}/products/{product_id}/stock?quantity_change=-3",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["quantity"] == 12

    def test_search_products(self, client: TestClient, db: Session, auth_headers):
        """Test searching products."""
        # Create test products
        products = [
            {
                "name": "Apple iPhone",
                "sku": "APPLE-001",
                "price": 999.00,
                "quantity": 10,
            },
            {
                "name": "Samsung Galaxy",
                "sku": "SAMSUNG-001",
                "price": 899.00,
                "quantity": 15,
            },
            {"name": "Apple iPad", "sku": "APPLE-002", "price": 599.00, "quantity": 20},
        ]

        for product_data in products:
            client.post(
                f"{settings.API_V1_STR}/products/",
                json=product_data,
                headers=auth_headers,
            )

        # Search for "Apple"
        response = client.get(
            f"{settings.API_V1_STR}/products/?search=Apple", headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 2
        for item in data["items"]:
            assert "apple" in item["name"].lower() or "apple" in item["sku"].lower()

    def test_filter_by_category(self, client: TestClient, db: Session, auth_headers):
        """Test filtering products by category."""
        # Create products with categories
        products = [
            {
                "name": "Product 1",
                "sku": "CAT-001",
                "price": 10.00,
                "quantity": 5,
                "category": "Electronics",
            },
            {
                "name": "Product 2",
                "sku": "CAT-002",
                "price": 20.00,
                "quantity": 10,
                "category": "Clothing",
            },
            {
                "name": "Product 3",
                "sku": "CAT-003",
                "price": 30.00,
                "quantity": 15,
                "category": "Electronics",
            },
        ]

        for product_data in products:
            client.post(
                f"{settings.API_V1_STR}/products/",
                json=product_data,
                headers=auth_headers,
            )

        # Filter by Electronics category
        response = client.get(
            f"{settings.API_V1_STR}/products/?category=Electronics",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 2
        for item in data["items"]:
            assert item["category"] == "Electronics"

    def test_get_low_stock_products(
        self, client: TestClient, db: Session, auth_headers
    ):
        """Test getting low stock products."""
        # Create products with different stock levels
        products = [
            {
                "name": "Low Stock",
                "sku": "LOW-001",
                "price": 10.00,
                "quantity": 2,
                "min_stock": 5,
            },
            {
                "name": "Good Stock",
                "sku": "GOOD-001",
                "price": 20.00,
                "quantity": 20,
                "min_stock": 5,
            },
            {
                "name": "Out of Stock",
                "sku": "OUT-001",
                "price": 30.00,
                "quantity": 0,
                "min_stock": 10,
            },
        ]

        for product_data in products:
            client.post(
                f"{settings.API_V1_STR}/products/",
                json=product_data,
                headers=auth_headers,
            )

        # Get low stock products
        response = client.get(
            f"{settings.API_V1_STR}/products/low-stock", headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2
        for item in data:
            assert item["quantity"] <= item["min_stock"]

    def test_product_permissions(
        self, client: TestClient, db: Session, auth_headers, superuser_headers
    ):
        """Test product permissions for regular user vs superuser."""
        # Create product as regular user
        product_data = {
            "name": "User Product",
            "sku": "PERM-001",
            "price": 50.00,
            "quantity": 10,
        }

        create_response = client.post(
            f"{settings.API_V1_STR}/products/", json=product_data, headers=auth_headers
        )
        product_id = create_response.json()["id"]

        # Regular user can update their own product
        update_response = client.put(
            f"{settings.API_V1_STR}/products/{product_id}",
            json={"name": "Updated by User"},
            headers=auth_headers,
        )
        assert update_response.status_code == 200

        # Superuser can also update any product
        update_response = client.put(
            f"{settings.API_V1_STR}/products/{product_id}",
            json={"name": "Updated by Admin"},
            headers=superuser_headers,
        )
        assert update_response.status_code == 200
