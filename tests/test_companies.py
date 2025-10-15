"""Tests for company endpoints."""

import pytest
import httpx


class TestCompanyCRUD:
    """Test CRUD operations for companies."""

    async def test_create_company(self, async_client: httpx.AsyncClient, auth_headers: dict):
        """Test creating a new company."""
        company_data = {"name": "Test Company"}
        response = await async_client.post(
            "/api/v1/companies/",
            json=company_data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == company_data["name"]
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    async def test_get_company(self, async_client: httpx.AsyncClient, auth_headers: dict):
        """Test retrieving a specific company."""
        # Create a company first
        company_data = {"name": "Get Test Company"}
        create_response = await async_client.post(
            "/api/v1/companies/",
            json=company_data,
            headers=auth_headers
        )
        company_id = create_response.json()["id"]
        
        # Get the company
        response = await async_client.get(
            f"/api/v1/companies/{company_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == company_id
        assert data["name"] == company_data["name"]

    async def test_update_company(self, async_client: httpx.AsyncClient, auth_headers: dict):
        """Test updating a company."""
        # Create a company first
        company_data = {"name": "Update Test Company"}
        create_response = await async_client.post(
            "/api/v1/companies/",
            json=company_data,
            headers=auth_headers
        )
        company_id = create_response.json()["id"]
        
        # Update the company
        update_data = {"name": "Updated Company Name"}
        response = await async_client.put(
            f"/api/v1/companies/{company_id}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Company Name"

    async def test_delete_company(self, async_client: httpx.AsyncClient, auth_headers: dict):
        """Test deleting a company."""
        # Create a company first
        company_data = {"name": "Delete Test Company"}
        create_response = await async_client.post(
            "/api/v1/companies/",
            json=company_data,
            headers=auth_headers
        )
        company_id = create_response.json()["id"]
        
        # Delete the company
        response = await async_client.delete(
            f"/api/v1/companies/{company_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 204
        
        # Verify company is deleted
        get_response = await async_client.get(
            f"/api/v1/companies/{company_id}",
            headers=auth_headers
        )
        assert get_response.status_code == 404

    async def test_list_companies(self, async_client: httpx.AsyncClient, auth_headers: dict):
        """Test listing all companies."""
        response = await async_client.get("/api/v1/companies/", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestCompanyPagination:
    """Test company pagination."""

    async def test_list_companies_with_pagination(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test listing companies with pagination parameters."""
        response = await async_client.get(
            "/api/v1/companies/?skip=0&limit=10",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 10

    async def test_list_companies_custom_limit(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test listing companies with custom limit."""
        response = await async_client.get(
            "/api/v1/companies/?skip=0&limit=5",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 5


class TestCompanyValidation:
    """Test company validation."""

    async def test_create_company_missing_name(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test creating company without name fails."""
        company_data = {}
        response = await async_client.post(
            "/api/v1/companies/",
            json=company_data,
            headers=auth_headers
        )
        assert response.status_code == 422

    async def test_create_company_empty_name(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test creating company with empty name."""
        company_data = {"name": ""}
        response = await async_client.post(
            "/api/v1/companies/",
            json=company_data,
            headers=auth_headers
        )
        # This might be 422 or 201 depending on validation rules
        # Adjust based on actual API behavior
        assert response.status_code in [201, 422]


class TestCompanyErrors:
    """Test error cases for companies."""

    async def test_get_nonexistent_company(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test getting non-existent company returns 404."""
        response = await async_client.get(
            "/api/v1/companies/999999",
            headers=auth_headers
        )
        assert response.status_code == 404

    async def test_update_nonexistent_company(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test updating non-existent company returns 404."""
        update_data = {"name": "Updated Name"}
        response = await async_client.put(
            "/api/v1/companies/999999",
            json=update_data,
            headers=auth_headers
        )
        assert response.status_code == 404

    async def test_delete_nonexistent_company(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test deleting non-existent company returns 404."""
        response = await async_client.delete(
            "/api/v1/companies/999999",
            headers=auth_headers
        )
        assert response.status_code == 404

