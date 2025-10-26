"""Tests for environment endpoints."""

import pytest
import httpx


class TestEnvironmentCRUD:
    """Test CRUD operations for environments."""

    async def test_create_environment(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test creating a new environment."""
        # First create a version and company
        version_data = {"name": "v1.0.0"}
        version_response = await async_client.post(
            "/api/v1/versions/",
            json=version_data,
            headers=auth_headers
        )
        version_id = version_response.json()["id"]
        
        company_data = {"name": "Test Company"}
        company_response = await async_client.post(
            "/api/v1/companies/",
            json=company_data,
            headers=auth_headers
        )
        company_id = company_response.json()["id"]
        
        # Create environment
        environment_data = {
            "name": "development",
            "description": "Development environment",
            "version_id": version_id,
            "company_id": company_id
        }
        response = await async_client.post(
            "/api/v1/environments/",
            json=environment_data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == environment_data["name"]
        assert data["description"] == environment_data["description"]
        assert data["version_id"] == version_id
        assert data["company_id"] == company_id
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    async def test_create_environment_without_description(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test creating an environment without description."""
        # Create version and company
        version_response = await async_client.post(
            "/api/v1/versions/",
            json={"name": "v1.1.0"},
            headers=auth_headers
        )
        version_id = version_response.json()["id"]
        
        company_response = await async_client.post(
            "/api/v1/companies/",
            json={"name": "Another Company"},
            headers=auth_headers
        )
        company_id = company_response.json()["id"]
        
        # Create environment without description
        environment_data = {
            "name": "staging",
            "version_id": version_id,
            "company_id": company_id
        }
        response = await async_client.post(
            "/api/v1/environments/",
            json=environment_data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == environment_data["name"]
        assert data["description"] is None

    async def test_create_multiple_environments(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test creating multiple environments."""
        # Create version and company
        version_response = await async_client.post(
            "/api/v1/versions/",
            json={"name": "v2.0.0"},
            headers=auth_headers
        )
        version_id = version_response.json()["id"]
        
        company_response = await async_client.post(
            "/api/v1/companies/",
            json={"name": "Multi Env Company"},
            headers=auth_headers
        )
        company_id = company_response.json()["id"]
        
        # Create multiple environments
        env1_data = {
            "name": "dev",
            "version_id": version_id,
            "company_id": company_id
        }
        env2_data = {
            "name": "prod",
            "version_id": version_id,
            "company_id": company_id
        }
        
        response1 = await async_client.post(
            "/api/v1/environments/",
            json=env1_data,
            headers=auth_headers
        )
        assert response1.status_code == 201
        
        response2 = await async_client.post(
            "/api/v1/environments/",
            json=env2_data,
            headers=auth_headers
        )
        assert response2.status_code == 201
        
        data1 = response1.json()
        data2 = response2.json()
        assert data1["name"] == "dev"
        assert data2["name"] == "prod"
        assert data1["id"] != data2["id"]

    async def test_get_environment(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test retrieving a specific environment."""
        # Create version and company
        version_response = await async_client.post(
            "/api/v1/versions/",
            json={"name": "v3.0.0"},
            headers=auth_headers
        )
        version_id = version_response.json()["id"]
        
        company_response = await async_client.post(
            "/api/v1/companies/",
            json={"name": "Get Env Company"},
            headers=auth_headers
        )
        company_id = company_response.json()["id"]
        
        # Create an environment
        environment_data = {
            "name": "test",
            "description": "Test environment",
            "version_id": version_id,
            "company_id": company_id
        }
        create_response = await async_client.post(
            "/api/v1/environments/",
            json=environment_data,
            headers=auth_headers
        )
        environment_id = create_response.json()["id"]
        
        # Get the environment
        response = await async_client.get(
            f"/api/v1/environments/{environment_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == environment_id
        assert data["name"] == environment_data["name"]
        assert data["description"] == environment_data["description"]

    async def test_update_environment(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test updating an environment."""
        # Create version and company
        version_response = await async_client.post(
            "/api/v1/versions/",
            json={"name": "v4.0.0"},
            headers=auth_headers
        )
        version_id = version_response.json()["id"]
        
        company_response = await async_client.post(
            "/api/v1/companies/",
            json={"name": "Update Env Company"},
            headers=auth_headers
        )
        company_id = company_response.json()["id"]
        
        # Create an environment
        environment_data = {
            "name": "old-env",
            "version_id": version_id,
            "company_id": company_id
        }
        create_response = await async_client.post(
            "/api/v1/environments/",
            json=environment_data,
            headers=auth_headers
        )
        environment_id = create_response.json()["id"]
        
        # Update the environment
        update_data = {
            "name": "new-env",
            "description": "Updated environment"
        }
        response = await async_client.put(
            f"/api/v1/environments/{environment_id}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "new-env"
        assert data["description"] == "Updated environment"
        assert data["id"] == environment_id

    async def test_delete_environment(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test deleting an environment."""
        # Create version and company
        version_response = await async_client.post(
            "/api/v1/versions/",
            json={"name": "v5.0.0"},
            headers=auth_headers
        )
        version_id = version_response.json()["id"]
        
        company_response = await async_client.post(
            "/api/v1/companies/",
            json={"name": "Delete Env Company"},
            headers=auth_headers
        )
        company_id = company_response.json()["id"]
        
        # Create an environment
        environment_data = {
            "name": "delete-me",
            "version_id": version_id,
            "company_id": company_id
        }
        create_response = await async_client.post(
            "/api/v1/environments/",
            json=environment_data,
            headers=auth_headers
        )
        environment_id = create_response.json()["id"]
        
        # Delete the environment
        response = await async_client.delete(
            f"/api/v1/environments/{environment_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 204
        
        # Verify environment is deleted
        get_response = await async_client.get(
            f"/api/v1/environments/{environment_id}",
            headers=auth_headers
        )
        assert get_response.status_code == 404

    async def test_list_environments(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test listing all environments."""
        response = await async_client.get(
            "/api/v1/environments/",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestEnvironmentPagination:
    """Test environment pagination."""

    async def test_list_environments_with_pagination(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test listing environments with pagination parameters."""
        response = await async_client.get(
            "/api/v1/environments/?skip=0&limit=10",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 10


class TestEnvironmentValidation:
    """Test environment validation."""

    async def test_create_environment_missing_name(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test creating environment without name fails."""
        # Create version and company
        version_response = await async_client.post(
            "/api/v1/versions/",
            json={"name": "v6.0.0"},
            headers=auth_headers
        )
        version_id = version_response.json()["id"]
        
        company_response = await async_client.post(
            "/api/v1/companies/",
            json={"name": "Validation Company"},
            headers=auth_headers
        )
        company_id = company_response.json()["id"]
        
        environment_data = {
            "version_id": version_id,
            "company_id": company_id
        }
        response = await async_client.post(
            "/api/v1/environments/",
            json=environment_data,
            headers=auth_headers
        )
        assert response.status_code == 422

    async def test_create_environment_missing_version_id(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test creating environment without version_id fails."""
        company_response = await async_client.post(
            "/api/v1/companies/",
            json={"name": "Validation Company 2"},
            headers=auth_headers
        )
        company_id = company_response.json()["id"]
        
        environment_data = {
            "name": "test-env",
            "company_id": company_id
        }
        response = await async_client.post(
            "/api/v1/environments/",
            json=environment_data,
            headers=auth_headers
        )
        assert response.status_code == 422

    async def test_create_environment_missing_company_id(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test creating environment without company_id fails."""
        version_response = await async_client.post(
            "/api/v1/versions/",
            json={"name": "v7.0.0"},
            headers=auth_headers
        )
        version_id = version_response.json()["id"]
        
        environment_data = {
            "name": "test-env",
            "version_id": version_id
        }
        response = await async_client.post(
            "/api/v1/environments/",
            json=environment_data,
            headers=auth_headers
        )
        assert response.status_code == 422

    async def test_create_duplicate_environment_same_version(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test creating duplicate environment names in same version fails."""
        # Create version and company
        version_response = await async_client.post(
            "/api/v1/versions/",
            json={"name": "v8.0.0"},
            headers=auth_headers
        )
        version_id = version_response.json()["id"]
        
        company_response = await async_client.post(
            "/api/v1/companies/",
            json={"name": "Duplicate Test Company"},
            headers=auth_headers
        )
        company_id = company_response.json()["id"]
        
        # Create first environment
        environment_data = {
            "name": "duplicate-env",
            "version_id": version_id,
            "company_id": company_id
        }
        response1 = await async_client.post(
            "/api/v1/environments/",
            json=environment_data,
            headers=auth_headers
        )
        assert response1.status_code == 201
        
        # Try to create duplicate
        response2 = await async_client.post(
            "/api/v1/environments/",
            json=environment_data,
            headers=auth_headers
        )
        # Should fail due to unique constraint
        assert response2.status_code in [400, 409, 500]  # Different DBs may return different codes

    async def test_create_same_name_different_versions(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test creating environments with same name in different versions succeeds."""
        # Create two versions
        version1_response = await async_client.post(
            "/api/v1/versions/",
            json={"name": "v9.0.0"},
            headers=auth_headers
        )
        version1_id = version1_response.json()["id"]
        
        version2_response = await async_client.post(
            "/api/v1/versions/",
            json={"name": "v9.1.0"},
            headers=auth_headers
        )
        version2_id = version2_response.json()["id"]
        
        # Create company
        company_response = await async_client.post(
            "/api/v1/companies/",
            json={"name": "Same Name Test Company"},
            headers=auth_headers
        )
        company_id = company_response.json()["id"]
        
        # Create environment in version 1
        env1_data = {
            "name": "production",
            "version_id": version1_id,
            "company_id": company_id
        }
        response1 = await async_client.post(
            "/api/v1/environments/",
            json=env1_data,
            headers=auth_headers
        )
        assert response1.status_code == 201
        
        # Create environment with same name in version 2 - should succeed
        env2_data = {
            "name": "production",
            "version_id": version2_id,
            "company_id": company_id
        }
        response2 = await async_client.post(
            "/api/v1/environments/",
            json=env2_data,
            headers=auth_headers
        )
        assert response2.status_code == 201
        
        # Verify they are different environments
        data1 = response1.json()
        data2 = response2.json()
        assert data1["id"] != data2["id"]
        assert data1["version_id"] != data2["version_id"]


class TestEnvironmentErrors:
    """Test error cases for environments."""

    async def test_get_nonexistent_environment(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test getting non-existent environment returns 404."""
        response = await async_client.get(
            "/api/v1/environments/999999",
            headers=auth_headers
        )
        assert response.status_code == 404

    async def test_update_nonexistent_environment(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test updating non-existent environment returns 404."""
        update_data = {"name": "updated"}
        response = await async_client.put(
            "/api/v1/environments/999999",
            json=update_data,
            headers=auth_headers
        )
        assert response.status_code == 404

    async def test_delete_nonexistent_environment(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test deleting non-existent environment returns 404."""
        response = await async_client.delete(
            "/api/v1/environments/999999",
            headers=auth_headers
        )
        assert response.status_code == 404


class TestEnvironmentRelationships:
    """Test environment relationships with other entities."""

    async def test_environment_belongs_to_version(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test environment is correctly linked to a version."""
        # Create version and company
        version_response = await async_client.post(
            "/api/v1/versions/",
            json={"name": "v10.0.0"},
            headers=auth_headers
        )
        version_id = version_response.json()["id"]
        
        company_response = await async_client.post(
            "/api/v1/companies/",
            json={"name": "Relationship Test Company"},
            headers=auth_headers
        )
        company_id = company_response.json()["id"]
        
        # Create environment
        environment_data = {
            "name": "relationship-test",
            "version_id": version_id,
            "company_id": company_id
        }
        env_response = await async_client.post(
            "/api/v1/environments/",
            json=environment_data,
            headers=auth_headers
        )
        
        assert env_response.status_code == 201
        env_data = env_response.json()
        assert env_data["version_id"] == version_id

    async def test_environment_belongs_to_company(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test environment is correctly linked to a company."""
        # Create version and company
        version_response = await async_client.post(
            "/api/v1/versions/",
            json={"name": "v11.0.0"},
            headers=auth_headers
        )
        version_id = version_response.json()["id"]
        
        company_response = await async_client.post(
            "/api/v1/companies/",
            json={"name": "Company Relationship Test"},
            headers=auth_headers
        )
        company_id = company_response.json()["id"]
        
        # Create environment
        environment_data = {
            "name": "company-link-test",
            "version_id": version_id,
            "company_id": company_id
        }
        env_response = await async_client.post(
            "/api/v1/environments/",
            json=environment_data,
            headers=auth_headers
        )
        
        assert env_response.status_code == 201
        env_data = env_response.json()
        assert env_data["company_id"] == company_id

