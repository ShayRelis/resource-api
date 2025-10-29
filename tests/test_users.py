"""Tests for user endpoints."""

import pytest
import httpx


class TestUserCRUD:
    """Test CRUD operations for users."""

    async def test_create_user(self, async_client: httpx.AsyncClient, auth_headers: dict):
        """Test creating a new user."""
        user_data = {
            "name": "CRUD Test User",
            "email": "crudtest@example.com",
            "password": "password123",
            "role": "user"
        }
        response = await async_client.post(
            "/api/v1/users/",
            json=user_data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["name"] == user_data["name"]
        assert "id" in data

    async def test_get_user(self, async_client: httpx.AsyncClient, auth_headers: dict):
        """Test retrieving a specific user."""
        # Create a user first
        user_data = {
            "name": "Get Test User",
            "email": "gettest@example.com",
            "password": "password123",
            "role": "user"
        }
        create_response = await async_client.post(
            "/api/v1/users/",
            json=user_data,
            headers=auth_headers
        )
        user_id = create_response.json()["id"]
        
        # Get the user
        response = await async_client.get(
            f"/api/v1/users/{user_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id
        assert data["email"] == user_data["email"]

    async def test_update_user(self, async_client: httpx.AsyncClient, auth_headers: dict):
        """Test updating a user."""
        # Create a user first
        user_data = {
            "name": "Update Test User",
            "email": "updatetest@example.com",
            "password": "password123",
            "role": "user"
        }
        create_response = await async_client.post(
            "/api/v1/users/",
            json=user_data,
            headers=auth_headers
        )
        user_id = create_response.json()["id"]
        
        # Update the user
        update_data = {"name": "Updated Name"}
        response = await async_client.put(
            f"/api/v1/users/{user_id}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Name"
        assert data["email"] == user_data["email"]  # Should remain unchanged

    async def test_delete_user(self, async_client: httpx.AsyncClient, auth_headers: dict):
        """Test deleting a user."""
        # Create a user first
        user_data = {
            "name": "Delete Test User",
            "email": "deletetest@example.com",
            "password": "password123",
            "role": "user"
        }
        create_response = await async_client.post(
            "/api/v1/users/",
            json=user_data,
            headers=auth_headers
        )
        user_id = create_response.json()["id"]
        
        # Delete the user
        response = await async_client.delete(
            f"/api/v1/users/{user_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 204
        
        # Verify user is deleted
        get_response = await async_client.get(
            f"/api/v1/users/{user_id}",
            headers=auth_headers
        )
        assert get_response.status_code == 404

    async def test_list_users(self, async_client: httpx.AsyncClient, auth_headers: dict):
        """Test listing all users."""
        response = await async_client.get("/api/v1/users/", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestUserPagination:
    """Test user pagination."""

    async def test_list_users_with_pagination(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test listing users with pagination parameters."""
        response = await async_client.get(
            "/api/v1/users/?skip=0&limit=5",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 5

    async def test_list_users_skip_parameter(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test skip parameter in pagination."""
        # Get first page
        response1 = await async_client.get(
            "/api/v1/users/?skip=0&limit=1",
            headers=auth_headers
        )
        
        # Get second page
        response2 = await async_client.get(
            "/api/v1/users/?skip=1&limit=1",
            headers=auth_headers
        )
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        data1 = response1.json()
        data2 = response2.json()
        
        # If there are at least 2 users, they should be different
        if len(data1) > 0 and len(data2) > 0:
            assert data1[0]["id"] != data2[0]["id"]


class TestUserValidation:
    """Test user validation."""

    async def test_create_user_invalid_email(self, async_client: httpx.AsyncClient, auth_headers: dict):
        """Test creating user with invalid email fails."""
        user_data = {
            "name": "Invalid Email",
            "email": "invalid-email",
            "password": "password123",
            "role": "user"
        }
        response = await async_client.post("/api/v1/users/", json=user_data, headers=auth_headers)
        assert response.status_code == 422

    async def test_create_user_missing_name(self, async_client: httpx.AsyncClient, auth_headers: dict):
        """Test creating user without name fails."""
        user_data = {
            "email": "noname@example.com",
            "password": "password123",
            "role": "user"
        }
        response = await async_client.post("/api/v1/users/", json=user_data, headers=auth_headers)
        assert response.status_code == 422

    async def test_create_user_missing_password(self, async_client: httpx.AsyncClient, auth_headers: dict):
        """Test creating user without password fails."""
        user_data = {
            "name": "No Password",
            "email": "nopassword@example.com",
            "role": "user"
        }
        response = await async_client.post("/api/v1/users/", json=user_data, headers=auth_headers)
        assert response.status_code == 422


class TestUserErrors:
    """Test error cases for users."""

    async def test_get_nonexistent_user(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test getting non-existent user returns 404."""
        response = await async_client.get(
            "/api/v1/users/999999",
            headers=auth_headers
        )
        assert response.status_code == 404

    async def test_update_nonexistent_user(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test updating non-existent user returns 404."""
        update_data = {"name": "Updated Name"}
        response = await async_client.put(
            "/api/v1/users/999999",
            json=update_data,
            headers=auth_headers
        )
        assert response.status_code == 404

    async def test_delete_nonexistent_user(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test deleting non-existent user returns 404."""
        response = await async_client.delete(
            "/api/v1/users/999999",
            headers=auth_headers
        )
        assert response.status_code == 404

