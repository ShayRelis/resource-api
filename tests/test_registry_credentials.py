"""Tests for registry credential endpoints."""

import pytest
import httpx


class TestRegistryCredentialCRUD:
    """Test CRUD operations for registry credentials."""

    async def test_create_registry_credential(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict,
        test_registry_provider: dict
    ):
        """Test creating a new registry credential."""
        credential_data = {
            "name": "AWS ECR Credentials",
            "access_key": "AKIAIOSFODNN7EXAMPLE",
            "secret_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
            "region": "us-east-1",
            "registry_provider_id": test_registry_provider["id"]
        }
        response = await async_client.post(
            "/api/v1/registry-credentials/",
            json=credential_data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == credential_data["name"]
        assert data["access_key"] == credential_data["access_key"]
        assert data["region"] == credential_data["region"]
        assert data["registry_provider_id"] == test_registry_provider["id"]
        assert "id" in data

    async def test_get_registry_credential(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict,
        test_registry_provider: dict
    ):
        """Test retrieving a specific registry credential."""
        # Create a credential first
        credential_data = {
            "name": "Get Test Credentials",
            "access_key": "test_access_key",
            "secret_key": "test_secret_key",
            "region": "eu-west-1",
            "registry_provider_id": test_registry_provider["id"]
        }
        create_response = await async_client.post(
            "/api/v1/registry-credentials/",
            json=credential_data,
            headers=auth_headers
        )
        credential_id = create_response.json()["id"]
        
        # Get the credential
        response = await async_client.get(
            f"/api/v1/registry-credentials/{credential_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == credential_id
        assert data["name"] == credential_data["name"]

    async def test_update_registry_credential(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict,
        test_registry_provider: dict
    ):
        """Test updating a registry credential."""
        # Create a credential first
        credential_data = {
            "name": "Update Test Credentials",
            "access_key": "old_access_key",
            "secret_key": "old_secret_key",
            "region": "us-west-2",
            "registry_provider_id": test_registry_provider["id"]
        }
        create_response = await async_client.post(
            "/api/v1/registry-credentials/",
            json=credential_data,
            headers=auth_headers
        )
        credential_id = create_response.json()["id"]
        
        # Update the credential
        update_data = {
            "access_key": "new_access_key",
            "region": "ap-southeast-1"
        }
        response = await async_client.put(
            f"/api/v1/registry-credentials/{credential_id}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["access_key"] == "new_access_key"
        assert data["region"] == "ap-southeast-1"

    async def test_delete_registry_credential(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict,
        test_registry_provider: dict
    ):
        """Test deleting a registry credential."""
        # Create a credential first
        credential_data = {
            "name": "Delete Test Credentials",
            "access_key": "delete_access_key",
            "secret_key": "delete_secret_key",
            "region": "us-east-1",
            "registry_provider_id": test_registry_provider["id"]
        }
        create_response = await async_client.post(
            "/api/v1/registry-credentials/",
            json=credential_data,
            headers=auth_headers
        )
        credential_id = create_response.json()["id"]
        
        # Delete the credential
        response = await async_client.delete(
            f"/api/v1/registry-credentials/{credential_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 204
        
        # Verify credential is deleted
        get_response = await async_client.get(
            f"/api/v1/registry-credentials/{credential_id}",
            headers=auth_headers
        )
        assert get_response.status_code == 404

    async def test_list_registry_credentials(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test listing all registry credentials."""
        response = await async_client.get(
            "/api/v1/registry-credentials/",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestRegistryCredentialPagination:
    """Test registry credential pagination."""

    async def test_list_registry_credentials_with_pagination(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test listing registry credentials with pagination parameters."""
        response = await async_client.get(
            "/api/v1/registry-credentials/?skip=0&limit=10",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 10


class TestRegistryCredentialValidation:
    """Test registry credential validation."""

    async def test_create_registry_credential_missing_name(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict,
        test_registry_provider: dict
    ):
        """Test creating credential without name fails."""
        credential_data = {
            "access_key": "access_key",
            "secret_key": "secret_key",
            "region": "us-east-1",
            "registry_provider_id": test_registry_provider["id"]
        }
        response = await async_client.post(
            "/api/v1/registry-credentials/",
            json=credential_data,
            headers=auth_headers
        )
        assert response.status_code == 422

    async def test_create_registry_credential_missing_keys(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict,
        test_registry_provider: dict
    ):
        """Test creating credential without access/secret keys fails."""
        credential_data = {
            "name": "No Keys Credentials",
            "region": "us-east-1",
            "registry_provider_id": test_registry_provider["id"]
        }
        response = await async_client.post(
            "/api/v1/registry-credentials/",
            json=credential_data,
            headers=auth_headers
        )
        assert response.status_code == 422


class TestRegistryCredentialRelationships:
    """Test registry credential relationships."""

    async def test_create_credential_with_invalid_provider_id(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test creating credential with non-existent provider_id fails."""
        credential_data = {
            "name": "Invalid Provider Credentials",
            "access_key": "access_key",
            "secret_key": "secret_key",
            "region": "us-east-1",
            "registry_provider_id": 999999
        }
        response = await async_client.post(
            "/api/v1/registry-credentials/",
            json=credential_data,
            headers=auth_headers
        )
        # Should return 404 or 400 for invalid foreign key
        assert response.status_code in [400, 404]


class TestRegistryCredentialErrors:
    """Test error cases for registry credentials."""

    async def test_get_nonexistent_registry_credential(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test getting non-existent credential returns 404."""
        response = await async_client.get(
            "/api/v1/registry-credentials/999999",
            headers=auth_headers
        )
        assert response.status_code == 404

    async def test_update_nonexistent_registry_credential(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test updating non-existent credential returns 404."""
        update_data = {"name": "Updated Name"}
        response = await async_client.put(
            "/api/v1/registry-credentials/999999",
            json=update_data,
            headers=auth_headers
        )
        assert response.status_code == 404

    async def test_delete_nonexistent_registry_credential(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test deleting non-existent credential returns 404."""
        response = await async_client.delete(
            "/api/v1/registry-credentials/999999",
            headers=auth_headers
        )
        assert response.status_code == 404

