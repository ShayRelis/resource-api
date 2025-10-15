"""Tests for registry endpoints."""

import pytest
import httpx


class TestRegistryCRUD:
    """Test CRUD operations for registries."""

    async def test_create_registry(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict,
        test_registry_provider: dict
    ):
        """Test creating a new registry."""
        registry_data = {
            "name": "My Docker Registry",
            "url": "https://registry.example.com",
            "is_private": True,
            "registry_provider_id": test_registry_provider["id"]
        }
        response = await async_client.post(
            "/api/v1/registries/",
            json=registry_data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == registry_data["name"]
        assert data["url"] == registry_data["url"]
        assert data["is_private"] == registry_data["is_private"]
        assert data["registry_provider_id"] == test_registry_provider["id"]
        assert "id" in data

    async def test_create_registry_public(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict,
        test_registry_provider: dict
    ):
        """Test creating a public registry."""
        registry_data = {
            "name": "Public Registry",
            "url": "https://public.registry.com",
            "is_private": False,
            "registry_provider_id": test_registry_provider["id"]
        }
        response = await async_client.post(
            "/api/v1/registries/",
            json=registry_data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["is_private"] is False

    async def test_get_registry(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict,
        test_registry_provider: dict
    ):
        """Test retrieving a specific registry."""
        # Create a registry first
        registry_data = {
            "name": "Get Test Registry",
            "url": "https://get.registry.com",
            "is_private": True,
            "registry_provider_id": test_registry_provider["id"]
        }
        create_response = await async_client.post(
            "/api/v1/registries/",
            json=registry_data,
            headers=auth_headers
        )
        registry_id = create_response.json()["id"]
        
        # Get the registry
        response = await async_client.get(
            f"/api/v1/registries/{registry_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == registry_id
        assert data["name"] == registry_data["name"]

    async def test_update_registry(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict,
        test_registry_provider: dict
    ):
        """Test updating a registry."""
        # Create a registry first
        registry_data = {
            "name": "Update Test Registry",
            "url": "https://update.registry.com",
            "is_private": True,
            "registry_provider_id": test_registry_provider["id"]
        }
        create_response = await async_client.post(
            "/api/v1/registries/",
            json=registry_data,
            headers=auth_headers
        )
        registry_id = create_response.json()["id"]
        
        # Update the registry
        update_data = {
            "name": "Updated Registry Name",
            "is_private": False
        }
        response = await async_client.put(
            f"/api/v1/registries/{registry_id}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Registry Name"
        assert data["is_private"] is False

    async def test_delete_registry(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict,
        test_registry_provider: dict
    ):
        """Test deleting a registry."""
        # Create a registry first
        registry_data = {
            "name": "Delete Test Registry",
            "url": "https://delete.registry.com",
            "is_private": True,
            "registry_provider_id": test_registry_provider["id"]
        }
        create_response = await async_client.post(
            "/api/v1/registries/",
            json=registry_data,
            headers=auth_headers
        )
        registry_id = create_response.json()["id"]
        
        # Delete the registry
        response = await async_client.delete(
            f"/api/v1/registries/{registry_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 204
        
        # Verify registry is deleted
        get_response = await async_client.get(
            f"/api/v1/registries/{registry_id}",
            headers=auth_headers
        )
        assert get_response.status_code == 404

    async def test_list_registries(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test listing all registries."""
        response = await async_client.get(
            "/api/v1/registries/",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestRegistryPagination:
    """Test registry pagination."""

    async def test_list_registries_with_pagination(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test listing registries with pagination parameters."""
        response = await async_client.get(
            "/api/v1/registries/?skip=0&limit=10",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 10


class TestRegistryValidation:
    """Test registry validation."""

    async def test_create_registry_missing_name(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict,
        test_registry_provider: dict
    ):
        """Test creating registry without name fails."""
        registry_data = {
            "url": "https://registry.com",
            "registry_provider_id": test_registry_provider["id"]
        }
        response = await async_client.post(
            "/api/v1/registries/",
            json=registry_data,
            headers=auth_headers
        )
        assert response.status_code == 422

    async def test_create_registry_missing_url(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict,
        test_registry_provider: dict
    ):
        """Test creating registry without URL fails."""
        registry_data = {
            "name": "No URL Registry",
            "registry_provider_id": test_registry_provider["id"]
        }
        response = await async_client.post(
            "/api/v1/registries/",
            json=registry_data,
            headers=auth_headers
        )
        assert response.status_code == 422

    async def test_create_registry_missing_provider_id(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test creating registry without registry_provider_id fails."""
        registry_data = {
            "name": "No Provider Registry",
            "url": "https://registry.com",
            "is_private": True
        }
        response = await async_client.post(
            "/api/v1/registries/",
            json=registry_data,
            headers=auth_headers
        )
        assert response.status_code == 422


class TestRegistryRelationships:
    """Test registry relationships with other entities."""

    async def test_create_registry_with_invalid_provider_id(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test creating registry with non-existent provider_id fails."""
        registry_data = {
            "name": "Invalid Provider Registry",
            "url": "https://registry.com",
            "is_private": True,
            "registry_provider_id": 999999
        }
        response = await async_client.post(
            "/api/v1/registries/",
            json=registry_data,
            headers=auth_headers
        )
        # Should return 404 or 400 for invalid foreign key
        assert response.status_code in [400, 404]

    async def test_create_registry_with_optional_credentials(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict,
        test_registry_provider: dict
    ):
        """Test creating registry with optional registry_credentials_id as None."""
        registry_data = {
            "name": "No Credentials Registry",
            "url": "https://registry.com",
            "is_private": True,
            "registry_provider_id": test_registry_provider["id"],
            "registry_credentials_id": None
        }
        response = await async_client.post(
            "/api/v1/registries/",
            json=registry_data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["registry_credentials_id"] is None


class TestRegistryErrors:
    """Test error cases for registries."""

    async def test_get_nonexistent_registry(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test getting non-existent registry returns 404."""
        response = await async_client.get(
            "/api/v1/registries/999999",
            headers=auth_headers
        )
        assert response.status_code == 404

    async def test_update_nonexistent_registry(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test updating non-existent registry returns 404."""
        update_data = {"name": "Updated Name"}
        response = await async_client.put(
            "/api/v1/registries/999999",
            json=update_data,
            headers=auth_headers
        )
        assert response.status_code == 404

    async def test_delete_nonexistent_registry(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test deleting non-existent registry returns 404."""
        response = await async_client.delete(
            "/api/v1/registries/999999",
            headers=auth_headers
        )
        assert response.status_code == 404

