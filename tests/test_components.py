"""Tests for component endpoints."""

import pytest
import httpx


class TestComponentCRUD:
    """Test CRUD operations for components."""

    async def test_create_component(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test creating a new component."""
        # First create a company for the component
        company_data = {"name": "Test Company"}
        company_response = await async_client.post(
            "/api/v1/companies/",
            json=company_data,
            headers=auth_headers
        )
        company_id = company_response.json()["id"]
        
        component_data = {
            "name": "API Service",
            "description": "Main API service component",
            "repository_url": "https://github.com/example/api-service",
            "is_managed": True,
            "is_third_party": False,
            "company_id": company_id,
            "team_ids": [],
            "tag_ids": [],
            "container_image_ids": [],
            "version_ids": []
        }
        response = await async_client.post(
            "/api/v1/components/",
            json=component_data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == component_data["name"]
        assert data["description"] == component_data["description"]
        assert data["repository_url"] == component_data["repository_url"]
        assert data["is_managed"] == component_data["is_managed"]
        assert data["is_third_party"] == component_data["is_third_party"]
        assert data["company_id"] == company_id
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    async def test_create_component_with_minimal_fields(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test creating a component with minimal required fields."""
        # First create a company
        company_data = {"name": "Minimal Company"}
        company_response = await async_client.post(
            "/api/v1/companies/",
            json=company_data,
            headers=auth_headers
        )
        company_id = company_response.json()["id"]
        
        component_data = {
            "name": "Minimal Component",
            "company_id": company_id
        }
        response = await async_client.post(
            "/api/v1/components/",
            json=component_data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == component_data["name"]
        assert data["description"] is None
        assert data["repository_url"] is None
        assert data["is_managed"] is True  # Default value
        assert data["is_third_party"] is None

    async def test_get_component(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test retrieving a specific component."""
        # Create a company first
        company_data = {"name": "Get Test Company"}
        company_response = await async_client.post(
            "/api/v1/companies/",
            json=company_data,
            headers=auth_headers
        )
        company_id = company_response.json()["id"]
        
        # Create a component
        component_data = {
            "name": "Frontend Service",
            "description": "React frontend application",
            "company_id": company_id
        }
        create_response = await async_client.post(
            "/api/v1/components/",
            json=component_data,
            headers=auth_headers
        )
        component_id = create_response.json()["id"]
        
        # Get the component
        response = await async_client.get(
            f"/api/v1/components/{component_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == component_id
        assert data["name"] == component_data["name"]
        assert data["description"] == component_data["description"]

    async def test_update_component(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test updating a component."""
        # Create a company first
        company_data = {"name": "Update Test Company"}
        company_response = await async_client.post(
            "/api/v1/companies/",
            json=company_data,
            headers=auth_headers
        )
        company_id = company_response.json()["id"]
        
        # Create a component
        component_data = {
            "name": "Backend Service",
            "description": "Initial description",
            "is_managed": True,
            "company_id": company_id
        }
        create_response = await async_client.post(
            "/api/v1/components/",
            json=component_data,
            headers=auth_headers
        )
        component_id = create_response.json()["id"]
        
        # Update the component
        update_data = {
            "description": "Updated backend service description",
            "repository_url": "https://github.com/example/backend",
            "is_third_party": False
        }
        response = await async_client.put(
            f"/api/v1/components/{component_id}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["description"] == "Updated backend service description"
        assert data["repository_url"] == "https://github.com/example/backend"
        assert data["is_third_party"] is False
        assert data["name"] == component_data["name"]  # Unchanged

    async def test_delete_component(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test deleting a component."""
        # Create a company first
        company_data = {"name": "Delete Test Company"}
        company_response = await async_client.post(
            "/api/v1/companies/",
            json=company_data,
            headers=auth_headers
        )
        company_id = company_response.json()["id"]
        
        # Create a component
        component_data = {
            "name": "Temporary Service",
            "company_id": company_id
        }
        create_response = await async_client.post(
            "/api/v1/components/",
            json=component_data,
            headers=auth_headers
        )
        component_id = create_response.json()["id"]
        
        # Delete the component
        response = await async_client.delete(
            f"/api/v1/components/{component_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 204
        
        # Verify component is deleted
        get_response = await async_client.get(
            f"/api/v1/components/{component_id}",
            headers=auth_headers
        )
        assert get_response.status_code == 404

    async def test_list_components(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test listing all components."""
        response = await async_client.get(
            "/api/v1/components/",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestComponentPagination:
    """Test component pagination."""

    async def test_list_components_with_pagination(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test listing components with pagination parameters."""
        response = await async_client.get(
            "/api/v1/components/?skip=0&limit=10",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 10


class TestComponentValidation:
    """Test component validation."""

    async def test_create_component_missing_name(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test creating component without name fails."""
        component_data = {
            "description": "No name component",
            "company_id": 1
        }
        response = await async_client.post(
            "/api/v1/components/",
            json=component_data,
            headers=auth_headers
        )
        assert response.status_code == 422

    async def test_create_component_missing_company_id(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test creating component without company_id fails."""
        component_data = {
            "name": "No Company Component"
        }
        response = await async_client.post(
            "/api/v1/components/",
            json=component_data,
            headers=auth_headers
        )
        assert response.status_code == 422

    async def test_create_component_default_is_managed(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test creating component without is_managed uses default True."""
        # Create a company first
        company_data = {"name": "Default Test Company"}
        company_response = await async_client.post(
            "/api/v1/companies/",
            json=company_data,
            headers=auth_headers
        )
        company_id = company_response.json()["id"]
        
        component_data = {
            "name": "Default Managed Component",
            "company_id": company_id
        }
        response = await async_client.post(
            "/api/v1/components/",
            json=component_data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["is_managed"] is True  # Default value


class TestComponentErrors:
    """Test error cases for components."""

    async def test_get_nonexistent_component(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test getting non-existent component returns 404."""
        response = await async_client.get(
            "/api/v1/components/999999",
            headers=auth_headers
        )
        assert response.status_code == 404

    async def test_update_nonexistent_component(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test updating non-existent component returns 404."""
        update_data = {"name": "Updated Name"}
        response = await async_client.put(
            "/api/v1/components/999999",
            json=update_data,
            headers=auth_headers
        )
        assert response.status_code == 404

    async def test_delete_nonexistent_component(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test deleting non-existent component returns 404."""
        response = await async_client.delete(
            "/api/v1/components/999999",
            headers=auth_headers
        )
        assert response.status_code == 404


class TestComponentAssociations:
    """Test component many-to-many associations."""

    async def test_create_component_with_teams(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test creating component with team associations."""
        # Create a company first
        company_data = {"name": "Association Test Company"}
        company_response = await async_client.post(
            "/api/v1/companies/",
            json=company_data,
            headers=auth_headers
        )
        company_id = company_response.json()["id"]
        
        # Create a team
        team_data = {"name": "DevOps Team", "company_id": company_id}
        team_response = await async_client.post(
            "/api/v1/teams/",
            json=team_data,
            headers=auth_headers
        )
        team_id = team_response.json()["id"]
        
        # Create component with team
        component_data = {
            "name": "Service with Team",
            "company_id": company_id,
            "team_ids": [team_id]
        }
        response = await async_client.post(
            "/api/v1/components/",
            json=component_data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert team_id in data["team_ids"]

    async def test_create_component_with_tags(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test creating component with tag associations."""
        # Create a company first
        company_data = {"name": "Tag Test Company"}
        company_response = await async_client.post(
            "/api/v1/companies/",
            json=company_data,
            headers=auth_headers
        )
        company_id = company_response.json()["id"]
        
        # Create a tag
        tag_data = {"name": "production", "company_id": company_id}
        tag_response = await async_client.post(
            "/api/v1/tags/",
            json=tag_data,
            headers=auth_headers
        )
        tag_id = tag_response.json()["id"]
        
        # Create component with tag
        component_data = {
            "name": "Service with Tag",
            "company_id": company_id,
            "tag_ids": [tag_id]
        }
        response = await async_client.post(
            "/api/v1/components/",
            json=component_data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert tag_id in data["tag_ids"]

    async def test_update_component_associations(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test updating component associations."""
        # Create a company first
        company_data = {"name": "Update Association Company"}
        company_response = await async_client.post(
            "/api/v1/companies/",
            json=company_data,
            headers=auth_headers
        )
        company_id = company_response.json()["id"]
        
        # Create component without associations
        component_data = {
            "name": "Service to Update",
            "company_id": company_id
        }
        create_response = await async_client.post(
            "/api/v1/components/",
            json=component_data,
            headers=auth_headers
        )
        component_id = create_response.json()["id"]
        
        # Create a team
        team_data = {"name": "New Team", "company_id": company_id}
        team_response = await async_client.post(
            "/api/v1/teams/",
            json=team_data,
            headers=auth_headers
        )
        team_id = team_response.json()["id"]
        
        # Update component with team association
        update_data = {
            "team_ids": [team_id]
        }
        response = await async_client.put(
            f"/api/v1/components/{component_id}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert team_id in data["team_ids"]

    async def test_delete_component_removes_associations(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test that deleting component removes its associations."""
        # Create a company first
        company_data = {"name": "Delete Association Company"}
        company_response = await async_client.post(
            "/api/v1/companies/",
            json=company_data,
            headers=auth_headers
        )
        company_id = company_response.json()["id"]
        
        # Create a team
        team_data = {"name": "Team to Associate", "company_id": company_id}
        team_response = await async_client.post(
            "/api/v1/teams/",
            json=team_data,
            headers=auth_headers
        )
        team_id = team_response.json()["id"]
        
        # Create component with team
        component_data = {
            "name": "Service to Delete",
            "company_id": company_id,
            "team_ids": [team_id]
        }
        create_response = await async_client.post(
            "/api/v1/components/",
            json=component_data,
            headers=auth_headers
        )
        component_id = create_response.json()["id"]
        
        # Verify component has associations
        get_response = await async_client.get(
            f"/api/v1/components/{component_id}",
            headers=auth_headers
        )
        assert team_id in get_response.json()["team_ids"]
        
        # Delete component
        delete_response = await async_client.delete(
            f"/api/v1/components/{component_id}",
            headers=auth_headers
        )
        assert delete_response.status_code == 204
        
        # Verify component is deleted
        verify_response = await async_client.get(
            f"/api/v1/components/{component_id}",
            headers=auth_headers
        )
        assert verify_response.status_code == 404

