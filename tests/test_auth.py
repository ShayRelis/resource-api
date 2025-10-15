"""Tests for authentication endpoints."""

import pytest
import httpx


class TestUserRegistration:
    """Test user registration endpoint."""

    async def test_register_user_success(self, async_client: httpx.AsyncClient):
        """Test successful user registration."""
        user_data = {
            "name": "New User",
            "email": "newuser@example.com",
            "password": "password123",
            "role": "user"
        }
        response = await async_client.post("/api/v1/auth/register", json=user_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["name"] == user_data["name"]
        assert "id" in data
        assert "password" not in data  # Password should not be returned

    async def test_register_duplicate_email(self, async_client: httpx.AsyncClient):
        """Test registration with duplicate email fails."""
        user_data = {
            "name": "User One",
            "email": "duplicate@example.com",
            "password": "password123",
            "role": "user"
        }
        
        # Register first time
        response1 = await async_client.post("/api/v1/auth/register", json=user_data)
        assert response1.status_code == 201
        
        # Try to register again with same email
        response2 = await async_client.post("/api/v1/auth/register", json=user_data)
        assert response2.status_code == 400
        assert "already registered" in response2.json()["detail"].lower()

    async def test_register_invalid_email(self, async_client: httpx.AsyncClient):
        """Test registration with invalid email format fails."""
        user_data = {
            "name": "Invalid Email User",
            "email": "not-an-email",
            "password": "password123",
            "role": "user"
        }
        response = await async_client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 422  # Validation error

    async def test_register_missing_required_fields(self, async_client: httpx.AsyncClient):
        """Test registration with missing required fields fails."""
        user_data = {
            "name": "Incomplete User"
            # Missing email and password
        }
        response = await async_client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 422  # Validation error

    async def test_register_with_optional_fields(self, async_client: httpx.AsyncClient):
        """Test registration with optional fields."""
        user_data = {
            "name": "Complete User",
            "email": "complete@example.com",
            "password": "password123",
            "phone": "+1234567890",
            "role": "admin"
        }
        response = await async_client.post("/api/v1/auth/register", json=user_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["phone"] == user_data["phone"]
        assert data["role"] == user_data["role"]


class TestUserLogin:
    """Test user login endpoint."""

    async def test_login_success(self, async_client: httpx.AsyncClient, test_user_data: dict):
        """Test successful login."""
        # Register user first
        await async_client.post("/api/v1/auth/register", json=test_user_data)
        
        # Login
        login_data = {
            "username": test_user_data["email"],
            "password": test_user_data["password"]
        }
        response = await async_client.post("/api/v1/auth/login", data=login_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    async def test_login_wrong_password(self, async_client: httpx.AsyncClient, test_user_data: dict):
        """Test login with wrong password fails."""
        # Register user first
        await async_client.post("/api/v1/auth/register", json=test_user_data)
        
        # Try to login with wrong password
        login_data = {
            "username": test_user_data["email"],
            "password": "wrongpassword"
        }
        response = await async_client.post("/api/v1/auth/login", data=login_data)
        
        assert response.status_code == 401
        assert "incorrect" in response.json()["detail"].lower()

    async def test_login_nonexistent_user(self, async_client: httpx.AsyncClient):
        """Test login with non-existent user fails."""
        login_data = {
            "username": "nonexistent@example.com",
            "password": "password123"
        }
        response = await async_client.post("/api/v1/auth/login", data=login_data)
        
        assert response.status_code == 401

    async def test_login_missing_credentials(self, async_client: httpx.AsyncClient):
        """Test login with missing credentials fails."""
        response = await async_client.post("/api/v1/auth/login", data={})
        assert response.status_code == 422  # Validation error


class TestProtectedEndpoints:
    """Test access to protected endpoints."""

    async def test_protected_endpoint_with_token(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test accessing protected endpoint with valid token."""
        response = await async_client.get("/api/v1/users/", headers=auth_headers)
        assert response.status_code == 200

    async def test_protected_endpoint_without_token(self, async_client: httpx.AsyncClient):
        """Test accessing protected endpoint without token fails."""
        response = await async_client.get("/api/v1/users/")
        assert response.status_code == 401

    async def test_protected_endpoint_invalid_token(self, async_client: httpx.AsyncClient):
        """Test accessing protected endpoint with invalid token fails."""
        headers = {"Authorization": "Bearer invalid_token_12345"}
        response = await async_client.get("/api/v1/users/", headers=headers)
        assert response.status_code == 401

