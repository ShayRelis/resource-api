"""Tests for version endpoints."""

import pytest
import httpx


class TestVersionCRUD:
    """Test CRUD operations for versions."""

    async def test_create_version(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test creating a new version."""
        version_data = {
            "name": "v1.0.0"
        }
        response = await async_client.post(
            "/api/v1/versions/",
            json=version_data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == version_data["name"]
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    async def test_create_multiple_versions(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test creating multiple versions."""
        version1_data = {"name": "v1.0"}
        version2_data = {"name": "v2.0"}
        
        response1 = await async_client.post(
            "/api/v1/versions/",
            json=version1_data,
            headers=auth_headers
        )
        assert response1.status_code == 201
        
        response2 = await async_client.post(
            "/api/v1/versions/",
            json=version2_data,
            headers=auth_headers
        )
        assert response2.status_code == 201
        
        data1 = response1.json()
        data2 = response2.json()
        assert data1["name"] == "v1.0"
        assert data2["name"] == "v2.0"
        assert data1["id"] != data2["id"]

    async def test_get_version(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test retrieving a specific version."""
        # Create a version first
        version_data = {"name": "v3.5.1"}
        create_response = await async_client.post(
            "/api/v1/versions/",
            json=version_data,
            headers=auth_headers
        )
        version_id = create_response.json()["id"]
        
        # Get the version
        response = await async_client.get(
            f"/api/v1/versions/{version_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == version_id
        assert data["name"] == version_data["name"]

    async def test_update_version(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test updating a version."""
        # Create a version first
        version_data = {"name": "v1.0.0-beta"}
        create_response = await async_client.post(
            "/api/v1/versions/",
            json=version_data,
            headers=auth_headers
        )
        version_id = create_response.json()["id"]
        
        # Update the version
        update_data = {"name": "v1.0.0-release"}
        response = await async_client.put(
            f"/api/v1/versions/{version_id}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "v1.0.0-release"
        assert data["id"] == version_id

    async def test_delete_version(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test deleting a version."""
        # Create a version first
        version_data = {"name": "v1.0.0-deprecated"}
        create_response = await async_client.post(
            "/api/v1/versions/",
            json=version_data,
            headers=auth_headers
        )
        version_id = create_response.json()["id"]
        
        # Delete the version
        response = await async_client.delete(
            f"/api/v1/versions/{version_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 204
        
        # Verify version is deleted
        get_response = await async_client.get(
            f"/api/v1/versions/{version_id}",
            headers=auth_headers
        )
        assert get_response.status_code == 404

    async def test_list_versions(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test listing all versions."""
        response = await async_client.get(
            "/api/v1/versions/",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestVersionPagination:
    """Test version pagination."""

    async def test_list_versions_with_pagination(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test listing versions with pagination parameters."""
        response = await async_client.get(
            "/api/v1/versions/?skip=0&limit=10",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 10


class TestVersionValidation:
    """Test version validation."""

    async def test_create_version_missing_name(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test creating version without name fails."""
        version_data = {}
        response = await async_client.post(
            "/api/v1/versions/",
            json=version_data,
            headers=auth_headers
        )
        assert response.status_code == 422


class TestVersionErrors:
    """Test error cases for versions."""

    async def test_get_nonexistent_version(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test getting non-existent version returns 404."""
        response = await async_client.get(
            "/api/v1/versions/999999",
            headers=auth_headers
        )
        assert response.status_code == 404

    async def test_update_nonexistent_version(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test updating non-existent version returns 404."""
        update_data = {"name": "v2.0"}
        response = await async_client.put(
            "/api/v1/versions/999999",
            json=update_data,
            headers=auth_headers
        )
        assert response.status_code == 404

    async def test_delete_nonexistent_version(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test deleting non-existent version returns 404."""
        response = await async_client.delete(
            "/api/v1/versions/999999",
            headers=auth_headers
        )
        assert response.status_code == 404

