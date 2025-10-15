"""Tests for tag endpoints."""

import pytest
import httpx


class TestTagCRUD:
    """Test CRUD operations for tags."""

    async def test_create_tag(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict,
        test_company: dict
    ):
        """Test creating a new tag."""
        tag_data = {
            "name": "production",
            "company_id": test_company["id"]
        }
        response = await async_client.post(
            "/api/v1/tags/",
            json=tag_data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == tag_data["name"]
        assert data["company_id"] == test_company["id"]
        assert "id" in data

    async def test_create_multiple_tags(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict,
        test_company: dict
    ):
        """Test creating multiple tags for the same company."""
        tags = ["production", "staging", "development"]
        
        for tag_name in tags:
            tag_data = {
                "name": tag_name,
                "company_id": test_company["id"]
            }
            response = await async_client.post(
                "/api/v1/tags/",
                json=tag_data,
                headers=auth_headers
            )
            assert response.status_code == 201
            assert response.json()["name"] == tag_name

    async def test_get_tag(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict,
        test_company: dict
    ):
        """Test retrieving a specific tag."""
        # Create a tag first
        tag_data = {
            "name": "get-test-tag",
            "company_id": test_company["id"]
        }
        create_response = await async_client.post(
            "/api/v1/tags/",
            json=tag_data,
            headers=auth_headers
        )
        tag_id = create_response.json()["id"]
        
        # Get the tag
        response = await async_client.get(
            f"/api/v1/tags/{tag_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == tag_id
        assert data["name"] == tag_data["name"]

    async def test_update_tag(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict,
        test_company: dict
    ):
        """Test updating a tag."""
        # Create a tag first
        tag_data = {
            "name": "old-tag-name",
            "company_id": test_company["id"]
        }
        create_response = await async_client.post(
            "/api/v1/tags/",
            json=tag_data,
            headers=auth_headers
        )
        tag_id = create_response.json()["id"]
        
        # Update the tag
        update_data = {"name": "new-tag-name"}
        response = await async_client.put(
            f"/api/v1/tags/{tag_id}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "new-tag-name"

    async def test_delete_tag(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict,
        test_company: dict
    ):
        """Test deleting a tag."""
        # Create a tag first
        tag_data = {
            "name": "delete-me",
            "company_id": test_company["id"]
        }
        create_response = await async_client.post(
            "/api/v1/tags/",
            json=tag_data,
            headers=auth_headers
        )
        tag_id = create_response.json()["id"]
        
        # Delete the tag
        response = await async_client.delete(
            f"/api/v1/tags/{tag_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 204
        
        # Verify tag is deleted
        get_response = await async_client.get(
            f"/api/v1/tags/{tag_id}",
            headers=auth_headers
        )
        assert get_response.status_code == 404

    async def test_list_tags(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test listing all tags."""
        response = await async_client.get(
            "/api/v1/tags/",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestTagPagination:
    """Test tag pagination."""

    async def test_list_tags_with_pagination(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test listing tags with pagination parameters."""
        response = await async_client.get(
            "/api/v1/tags/?skip=0&limit=10",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 10


class TestTagValidation:
    """Test tag validation."""

    async def test_create_tag_missing_name(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict,
        test_company: dict
    ):
        """Test creating tag without name fails."""
        tag_data = {"company_id": test_company["id"]}
        response = await async_client.post(
            "/api/v1/tags/",
            json=tag_data,
            headers=auth_headers
        )
        assert response.status_code == 422

    async def test_create_tag_missing_company_id(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test creating tag without company_id fails."""
        tag_data = {"name": "orphan-tag"}
        response = await async_client.post(
            "/api/v1/tags/",
            json=tag_data,
            headers=auth_headers
        )
        assert response.status_code == 422


class TestTagRelationships:
    """Test tag relationships with other entities."""

    async def test_create_tag_with_invalid_company_id(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test creating tag with non-existent company_id fails."""
        tag_data = {
            "name": "invalid-company-tag",
            "company_id": 999999
        }
        response = await async_client.post(
            "/api/v1/tags/",
            json=tag_data,
            headers=auth_headers
        )
        # Should return 404 or 400 for invalid foreign key
        assert response.status_code in [400, 404]


class TestTagErrors:
    """Test error cases for tags."""

    async def test_get_nonexistent_tag(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test getting non-existent tag returns 404."""
        response = await async_client.get(
            "/api/v1/tags/999999",
            headers=auth_headers
        )
        assert response.status_code == 404

    async def test_update_nonexistent_tag(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test updating non-existent tag returns 404."""
        update_data = {"name": "Updated Name"}
        response = await async_client.put(
            "/api/v1/tags/999999",
            json=update_data,
            headers=auth_headers
        )
        assert response.status_code == 404

    async def test_delete_nonexistent_tag(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test deleting non-existent tag returns 404."""
        response = await async_client.delete(
            "/api/v1/tags/999999",
            headers=auth_headers
        )
        assert response.status_code == 404

