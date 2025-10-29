"""Tests for authentication endpoints."""

import pytest
import httpx
from typing import Dict


class TestUserLogin:
    """Test user login endpoint."""

    async def test_login_success(self, async_client: httpx.AsyncClient, test_user: Dict[str, str]):
        """Test successful login."""
        # Login with test user created by fixture
        login_data = {
            "username": test_user["email"],
            "password": test_user["password"]
        }
        response = await async_client.post("/api/v1/auth/login", data=login_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    async def test_login_wrong_password(self, async_client: httpx.AsyncClient, test_user: Dict[str, str]):
        """Test login with wrong password fails."""
        # Try to login with wrong password
        login_data = {
            "username": test_user["email"],
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

