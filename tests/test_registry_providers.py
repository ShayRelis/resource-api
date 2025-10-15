"""Tests for registry provider endpoints."""

import pytest
import httpx


class TestRegistryProviderCRUD:
    """Test CRUD operations for registry providers."""

    async def test_create_registry_provider(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test creating a new registry provider."""
        provider_data = {"name": "Docker Hub"}
        response = await async_client.post(
            "/api/v1/registry-providers/",
            json=provider_data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == provider_data["name"]
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    async def test_get_registry_provider(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test retrieving a specific registry provider."""
        # Create a provider first
        provider_data = {"name": "ECR"}
        create_response = await async_client.post(
            "/api/v1/registry-providers/",
            json=provider_data,
            headers=auth_headers
        )
        provider_id = create_response.json()["id"]
        
        # Get the provider
        response = await async_client.get(
            f"/api/v1/registry-providers/{provider_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == provider_id
        assert data["name"] == provider_data["name"]

    async def test_update_registry_provider(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test updating a registry provider."""
        # Create a provider first
        provider_data = {"name": "GCR"}
        create_response = await async_client.post(
            "/api/v1/registry-providers/",
            json=provider_data,
            headers=auth_headers
        )
        provider_id = create_response.json()["id"]
        
        # Update the provider
        update_data = {"name": "Google Container Registry"}
        response = await async_client.put(
            f"/api/v1/registry-providers/{provider_id}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Google Container Registry"

    async def test_delete_registry_provider(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test deleting a registry provider."""
        # Create a provider first
        provider_data = {"name": "Delete Registry Provider"}
        create_response = await async_client.post(
            "/api/v1/registry-providers/",
            json=provider_data,
            headers=auth_headers
        )
        provider_id = create_response.json()["id"]
        
        # Delete the provider
        response = await async_client.delete(
            f"/api/v1/registry-providers/{provider_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 204
        
        # Verify provider is deleted
        get_response = await async_client.get(
            f"/api/v1/registry-providers/{provider_id}",
            headers=auth_headers
        )
        assert get_response.status_code == 404

    async def test_list_registry_providers(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test listing all registry providers."""
        response = await async_client.get(
            "/api/v1/registry-providers/",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestRegistryProviderPagination:
    """Test registry provider pagination."""

    async def test_list_registry_providers_with_pagination(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test listing registry providers with pagination parameters."""
        response = await async_client.get(
            "/api/v1/registry-providers/?skip=0&limit=10",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 10


class TestRegistryProviderValidation:
    """Test registry provider validation."""

    async def test_create_registry_provider_missing_name(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test creating registry provider without name fails."""
        provider_data = {}
        response = await async_client.post(
            "/api/v1/registry-providers/",
            json=provider_data,
            headers=auth_headers
        )
        assert response.status_code == 422


class TestRegistryProviderErrors:
    """Test error cases for registry providers."""

    async def test_get_nonexistent_registry_provider(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test getting non-existent registry provider returns 404."""
        response = await async_client.get(
            "/api/v1/registry-providers/999999",
            headers=auth_headers
        )
        assert response.status_code == 404

    async def test_update_nonexistent_registry_provider(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test updating non-existent registry provider returns 404."""
        update_data = {"name": "Updated Name"}
        response = await async_client.put(
            "/api/v1/registry-providers/999999",
            json=update_data,
            headers=auth_headers
        )
        assert response.status_code == 404

    async def test_delete_nonexistent_registry_provider(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test deleting non-existent registry provider returns 404."""
        response = await async_client.delete(
            "/api/v1/registry-providers/999999",
            headers=auth_headers
        )
        assert response.status_code == 404

