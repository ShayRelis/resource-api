"""Tests for container image endpoints."""

import pytest
import httpx
from datetime import datetime


class TestContainerImageCRUD:
    """Test CRUD operations for container images."""

    async def test_create_container_image(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict,
        test_registry: dict
    ):
        """Test creating a new container image."""
        image_data = {
            "name": "myapp",
            "tag": "v1.0.0",
            "registry_id": test_registry["id"],
            "pushed_at": datetime.now().isoformat()
        }
        response = await async_client.post(
            "/api/v1/container-images/",
            json=image_data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == image_data["name"]
        assert data["tag"] == image_data["tag"]
        assert data["registry_id"] == test_registry["id"]
        assert "id" in data

    async def test_create_container_image_different_tags(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict,
        test_registry: dict
    ):
        """Test creating multiple images with different tags."""
        base_data = {
            "name": "webapp",
            "registry_id": test_registry["id"],
            "pushed_at": datetime.now().isoformat()
        }
        
        # Create image with tag v1
        image1_data = {**base_data, "tag": "v1"}
        response1 = await async_client.post(
            "/api/v1/container-images/",
            json=image1_data,
            headers=auth_headers
        )
        assert response1.status_code == 201
        
        # Create image with tag v2
        image2_data = {**base_data, "tag": "v2"}
        response2 = await async_client.post(
            "/api/v1/container-images/",
            json=image2_data,
            headers=auth_headers
        )
        assert response2.status_code == 201
        
        data1 = response1.json()
        data2 = response2.json()
        assert data1["tag"] == "v1"
        assert data2["tag"] == "v2"

    async def test_get_container_image(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict,
        test_registry: dict
    ):
        """Test retrieving a specific container image."""
        # Create an image first
        image_data = {
            "name": "testapp",
            "tag": "latest",
            "registry_id": test_registry["id"],
            "pushed_at": datetime.now().isoformat()
        }
        create_response = await async_client.post(
            "/api/v1/container-images/",
            json=image_data,
            headers=auth_headers
        )
        image_id = create_response.json()["id"]
        
        # Get the image
        response = await async_client.get(
            f"/api/v1/container-images/{image_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == image_id
        assert data["name"] == image_data["name"]
        assert data["tag"] == image_data["tag"]

    async def test_update_container_image(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict,
        test_registry: dict
    ):
        """Test updating a container image."""
        # Create an image first
        image_data = {
            "name": "updateapp",
            "tag": "v1.0",
            "registry_id": test_registry["id"],
            "pushed_at": datetime.now().isoformat()
        }
        create_response = await async_client.post(
            "/api/v1/container-images/",
            json=image_data,
            headers=auth_headers
        )
        image_id = create_response.json()["id"]
        
        # Update the image
        update_data = {"tag": "v1.1"}
        response = await async_client.put(
            f"/api/v1/container-images/{image_id}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["tag"] == "v1.1"
        assert data["name"] == image_data["name"]  # Should remain unchanged

    async def test_delete_container_image(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict,
        test_registry: dict
    ):
        """Test deleting a container image."""
        # Create an image first
        image_data = {
            "name": "deleteapp",
            "tag": "remove",
            "registry_id": test_registry["id"],
            "pushed_at": datetime.now().isoformat()
        }
        create_response = await async_client.post(
            "/api/v1/container-images/",
            json=image_data,
            headers=auth_headers
        )
        image_id = create_response.json()["id"]
        
        # Delete the image
        response = await async_client.delete(
            f"/api/v1/container-images/{image_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 204
        
        # Verify image is deleted
        get_response = await async_client.get(
            f"/api/v1/container-images/{image_id}",
            headers=auth_headers
        )
        assert get_response.status_code == 404

    async def test_list_container_images(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test listing all container images."""
        response = await async_client.get(
            "/api/v1/container-images/",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestContainerImagePagination:
    """Test container image pagination."""

    async def test_list_container_images_with_pagination(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test listing container images with pagination parameters."""
        response = await async_client.get(
            "/api/v1/container-images/?skip=0&limit=10",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 10


class TestContainerImageValidation:
    """Test container image validation."""

    async def test_create_container_image_missing_name(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict,
        test_registry: dict
    ):
        """Test creating image without name fails."""
        image_data = {
            "tag": "v1.0",
            "registry_id": test_registry["id"],
            "pushed_at": datetime.now().isoformat()
        }
        response = await async_client.post(
            "/api/v1/container-images/",
            json=image_data,
            headers=auth_headers
        )
        assert response.status_code == 422

    async def test_create_container_image_missing_tag(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict,
        test_registry: dict
    ):
        """Test creating image without tag fails."""
        image_data = {
            "name": "notag",
            "registry_id": test_registry["id"],
            "pushed_at": datetime.now().isoformat()
        }
        response = await async_client.post(
            "/api/v1/container-images/",
            json=image_data,
            headers=auth_headers
        )
        assert response.status_code == 422

    async def test_create_container_image_missing_registry_id(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test creating image without registry_id fails."""
        image_data = {
            "name": "noregistry",
            "tag": "v1.0",
            "pushed_at": datetime.now().isoformat()
        }
        response = await async_client.post(
            "/api/v1/container-images/",
            json=image_data,
            headers=auth_headers
        )
        assert response.status_code == 422

    async def test_create_container_image_missing_pushed_at(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict,
        test_registry: dict
    ):
        """Test creating image without pushed_at fails."""
        image_data = {
            "name": "nopushedat",
            "tag": "v1.0",
            "registry_id": test_registry["id"]
        }
        response = await async_client.post(
            "/api/v1/container-images/",
            json=image_data,
            headers=auth_headers
        )
        assert response.status_code == 422


class TestContainerImageRelationships:
    """Test container image relationships."""

    async def test_create_container_image_with_invalid_registry_id(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test creating image with non-existent registry_id fails."""
        image_data = {
            "name": "invalidregistry",
            "tag": "v1.0",
            "registry_id": 999999,
            "pushed_at": datetime.now().isoformat()
        }
        response = await async_client.post(
            "/api/v1/container-images/",
            json=image_data,
            headers=auth_headers
        )
        # Should return 404 or 400 for invalid foreign key
        assert response.status_code in [400, 404]


class TestContainerImageErrors:
    """Test error cases for container images."""

    async def test_get_nonexistent_container_image(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test getting non-existent image returns 404."""
        response = await async_client.get(
            "/api/v1/container-images/999999",
            headers=auth_headers
        )
        assert response.status_code == 404

    async def test_update_nonexistent_container_image(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test updating non-existent image returns 404."""
        update_data = {"tag": "v2.0"}
        response = await async_client.put(
            "/api/v1/container-images/999999",
            json=update_data,
            headers=auth_headers
        )
        assert response.status_code == 404

    async def test_delete_nonexistent_container_image(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test deleting non-existent image returns 404."""
        response = await async_client.delete(
            "/api/v1/container-images/999999",
            headers=auth_headers
        )
        assert response.status_code == 404

