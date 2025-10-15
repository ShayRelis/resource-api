"""Tests for service type endpoints."""

import pytest
import httpx


class TestServiceTypeCRUD:
    """Test CRUD operations for service types."""

    async def test_create_service_type(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test creating a new service type."""
        service_type_data = {
            "name": "API Gateway",
            "description": "RESTful API Gateway Service",
            "is_managed": True
        }
        response = await async_client.post(
            "/api/v1/service-types/",
            json=service_type_data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == service_type_data["name"]
        assert data["description"] == service_type_data["description"]
        assert data["is_managed"] == service_type_data["is_managed"]
        assert "id" in data

    async def test_create_service_type_unmanaged(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test creating an unmanaged service type."""
        service_type_data = {
            "name": "Custom Service",
            "description": "Custom unmanaged service",
            "is_managed": False
        }
        response = await async_client.post(
            "/api/v1/service-types/",
            json=service_type_data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["is_managed"] is False

    async def test_get_service_type(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test retrieving a specific service type."""
        # Create a service type first
        service_type_data = {
            "name": "Load Balancer",
            "description": "Application Load Balancer",
            "is_managed": True
        }
        create_response = await async_client.post(
            "/api/v1/service-types/",
            json=service_type_data,
            headers=auth_headers
        )
        service_type_id = create_response.json()["id"]
        
        # Get the service type
        response = await async_client.get(
            f"/api/v1/service-types/{service_type_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == service_type_id
        assert data["name"] == service_type_data["name"]

    async def test_update_service_type(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test updating a service type."""
        # Create a service type first
        service_type_data = {
            "name": "Database",
            "description": "Relational Database",
            "is_managed": True
        }
        create_response = await async_client.post(
            "/api/v1/service-types/",
            json=service_type_data,
            headers=auth_headers
        )
        service_type_id = create_response.json()["id"]
        
        # Update the service type
        update_data = {
            "description": "Managed Relational Database Service",
            "is_managed": True
        }
        response = await async_client.put(
            f"/api/v1/service-types/{service_type_id}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["description"] == "Managed Relational Database Service"

    async def test_delete_service_type(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test deleting a service type."""
        # Create a service type first
        service_type_data = {
            "name": "Cache",
            "description": "In-memory Cache Service",
            "is_managed": True
        }
        create_response = await async_client.post(
            "/api/v1/service-types/",
            json=service_type_data,
            headers=auth_headers
        )
        service_type_id = create_response.json()["id"]
        
        # Delete the service type
        response = await async_client.delete(
            f"/api/v1/service-types/{service_type_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 204
        
        # Verify service type is deleted
        get_response = await async_client.get(
            f"/api/v1/service-types/{service_type_id}",
            headers=auth_headers
        )
        assert get_response.status_code == 404

    async def test_list_service_types(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test listing all service types."""
        response = await async_client.get(
            "/api/v1/service-types/",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestServiceTypePagination:
    """Test service type pagination."""

    async def test_list_service_types_with_pagination(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test listing service types with pagination parameters."""
        response = await async_client.get(
            "/api/v1/service-types/?skip=0&limit=10",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 10


class TestServiceTypeValidation:
    """Test service type validation."""

    async def test_create_service_type_missing_name(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test creating service type without name fails."""
        service_type_data = {
            "description": "No name service",
            "is_managed": True
        }
        response = await async_client.post(
            "/api/v1/service-types/",
            json=service_type_data,
            headers=auth_headers
        )
        assert response.status_code == 422

    async def test_create_service_type_missing_description(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test creating service type without description fails."""
        service_type_data = {
            "name": "No Description Service",
            "is_managed": True
        }
        response = await async_client.post(
            "/api/v1/service-types/",
            json=service_type_data,
            headers=auth_headers
        )
        assert response.status_code == 422

    async def test_create_service_type_default_is_managed(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test creating service type without is_managed uses default True."""
        service_type_data = {
            "name": "Default Managed",
            "description": "Uses default is_managed value"
        }
        response = await async_client.post(
            "/api/v1/service-types/",
            json=service_type_data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["is_managed"] is True  # Default value


class TestServiceTypeErrors:
    """Test error cases for service types."""

    async def test_get_nonexistent_service_type(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test getting non-existent service type returns 404."""
        response = await async_client.get(
            "/api/v1/service-types/999999",
            headers=auth_headers
        )
        assert response.status_code == 404

    async def test_update_nonexistent_service_type(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test updating non-existent service type returns 404."""
        update_data = {"name": "Updated Name"}
        response = await async_client.put(
            "/api/v1/service-types/999999",
            json=update_data,
            headers=auth_headers
        )
        assert response.status_code == 404

    async def test_delete_nonexistent_service_type(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test deleting non-existent service type returns 404."""
        response = await async_client.delete(
            "/api/v1/service-types/999999",
            headers=auth_headers
        )
        assert response.status_code == 404

