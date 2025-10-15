"""Tests for cloud provider endpoints."""

import pytest
import httpx


class TestCloudProviderCRUD:
    """Test CRUD operations for cloud providers."""

    async def test_create_cloud_provider(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test creating a new cloud provider."""
        provider_data = {"name": "AWS Test"}
        response = await async_client.post(
            "/api/v1/cloud-providers/",
            json=provider_data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == provider_data["name"]
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    async def test_get_cloud_provider(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test retrieving a specific cloud provider."""
        # Create a provider first
        provider_data = {"name": "GCP Test"}
        create_response = await async_client.post(
            "/api/v1/cloud-providers/",
            json=provider_data,
            headers=auth_headers
        )
        provider_id = create_response.json()["id"]
        
        # Get the provider
        response = await async_client.get(
            f"/api/v1/cloud-providers/{provider_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == provider_id
        assert data["name"] == provider_data["name"]

    async def test_update_cloud_provider(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test updating a cloud provider."""
        # Create a provider first
        provider_data = {"name": "Azure Test"}
        create_response = await async_client.post(
            "/api/v1/cloud-providers/",
            json=provider_data,
            headers=auth_headers
        )
        provider_id = create_response.json()["id"]
        
        # Update the provider
        update_data = {"name": "Azure Updated"}
        response = await async_client.put(
            f"/api/v1/cloud-providers/{provider_id}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Azure Updated"

    async def test_delete_cloud_provider(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test deleting a cloud provider."""
        # Create a provider first
        provider_data = {"name": "Delete Cloud Provider"}
        create_response = await async_client.post(
            "/api/v1/cloud-providers/",
            json=provider_data,
            headers=auth_headers
        )
        provider_id = create_response.json()["id"]
        
        # Delete the provider
        response = await async_client.delete(
            f"/api/v1/cloud-providers/{provider_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 204
        
        # Verify provider is deleted
        get_response = await async_client.get(
            f"/api/v1/cloud-providers/{provider_id}",
            headers=auth_headers
        )
        assert get_response.status_code == 404

    async def test_list_cloud_providers(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test listing all cloud providers."""
        response = await async_client.get(
            "/api/v1/cloud-providers/",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestCloudProviderPagination:
    """Test cloud provider pagination."""

    async def test_list_cloud_providers_with_pagination(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test listing cloud providers with pagination parameters."""
        response = await async_client.get(
            "/api/v1/cloud-providers/?skip=0&limit=10",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 10


class TestCloudProviderValidation:
    """Test cloud provider validation."""

    async def test_create_cloud_provider_missing_name(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test creating cloud provider without name fails."""
        provider_data = {}
        response = await async_client.post(
            "/api/v1/cloud-providers/",
            json=provider_data,
            headers=auth_headers
        )
        assert response.status_code == 422


class TestCloudProviderErrors:
    """Test error cases for cloud providers."""

    async def test_get_nonexistent_cloud_provider(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test getting non-existent cloud provider returns 404."""
        response = await async_client.get(
            "/api/v1/cloud-providers/999999",
            headers=auth_headers
        )
        assert response.status_code == 404

    async def test_update_nonexistent_cloud_provider(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test updating non-existent cloud provider returns 404."""
        update_data = {"name": "Updated Name"}
        response = await async_client.put(
            "/api/v1/cloud-providers/999999",
            json=update_data,
            headers=auth_headers
        )
        assert response.status_code == 404

    async def test_delete_nonexistent_cloud_provider(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test deleting non-existent cloud provider returns 404."""
        response = await async_client.delete(
            "/api/v1/cloud-providers/999999",
            headers=auth_headers
        )
        assert response.status_code == 404

