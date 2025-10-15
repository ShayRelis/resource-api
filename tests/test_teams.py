"""Tests for team endpoints."""

import pytest
import httpx


class TestTeamCRUD:
    """Test CRUD operations for teams."""

    async def test_create_team(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict,
        test_company: dict
    ):
        """Test creating a new team."""
        team_data = {
            "name": "Test Team",
            "company_id": test_company["id"]
        }
        response = await async_client.post(
            "/api/v1/teams/",
            json=team_data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == team_data["name"]
        assert data["company_id"] == test_company["id"]
        assert "id" in data

    async def test_get_team(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict,
        test_company: dict
    ):
        """Test retrieving a specific team."""
        # Create a team first
        team_data = {
            "name": "Get Test Team",
            "company_id": test_company["id"]
        }
        create_response = await async_client.post(
            "/api/v1/teams/",
            json=team_data,
            headers=auth_headers
        )
        team_id = create_response.json()["id"]
        
        # Get the team
        response = await async_client.get(
            f"/api/v1/teams/{team_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == team_id
        assert data["name"] == team_data["name"]

    async def test_update_team(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict,
        test_company: dict
    ):
        """Test updating a team."""
        # Create a team first
        team_data = {
            "name": "Update Test Team",
            "company_id": test_company["id"]
        }
        create_response = await async_client.post(
            "/api/v1/teams/",
            json=team_data,
            headers=auth_headers
        )
        team_id = create_response.json()["id"]
        
        # Update the team
        update_data = {"name": "Updated Team Name"}
        response = await async_client.put(
            f"/api/v1/teams/{team_id}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Team Name"

    async def test_delete_team(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict,
        test_company: dict
    ):
        """Test deleting a team."""
        # Create a team first
        team_data = {
            "name": "Delete Test Team",
            "company_id": test_company["id"]
        }
        create_response = await async_client.post(
            "/api/v1/teams/",
            json=team_data,
            headers=auth_headers
        )
        team_id = create_response.json()["id"]
        
        # Delete the team
        response = await async_client.delete(
            f"/api/v1/teams/{team_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 204
        
        # Verify team is deleted
        get_response = await async_client.get(
            f"/api/v1/teams/{team_id}",
            headers=auth_headers
        )
        assert get_response.status_code == 404

    async def test_list_teams(self, async_client: httpx.AsyncClient, auth_headers: dict):
        """Test listing all teams."""
        response = await async_client.get("/api/v1/teams/", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestTeamPagination:
    """Test team pagination."""

    async def test_list_teams_with_pagination(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test listing teams with pagination parameters."""
        response = await async_client.get(
            "/api/v1/teams/?skip=0&limit=10",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 10


class TestTeamValidation:
    """Test team validation."""

    async def test_create_team_missing_name(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict,
        test_company: dict
    ):
        """Test creating team without name fails."""
        team_data = {"company_id": test_company["id"]}
        response = await async_client.post(
            "/api/v1/teams/",
            json=team_data,
            headers=auth_headers
        )
        assert response.status_code == 422

    async def test_create_team_missing_company_id(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test creating team without company_id fails."""
        team_data = {"name": "No Company Team"}
        response = await async_client.post(
            "/api/v1/teams/",
            json=team_data,
            headers=auth_headers
        )
        assert response.status_code == 422


class TestTeamRelationships:
    """Test team relationships with other entities."""

    async def test_create_team_with_invalid_company_id(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test creating team with non-existent company_id fails."""
        team_data = {
            "name": "Invalid Company Team",
            "company_id": 999999
        }
        response = await async_client.post(
            "/api/v1/teams/",
            json=team_data,
            headers=auth_headers
        )
        # Should return 404 or 400 for invalid foreign key
        assert response.status_code in [400, 404]


class TestTeamErrors:
    """Test error cases for teams."""

    async def test_get_nonexistent_team(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test getting non-existent team returns 404."""
        response = await async_client.get(
            "/api/v1/teams/999999",
            headers=auth_headers
        )
        assert response.status_code == 404

    async def test_update_nonexistent_team(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test updating non-existent team returns 404."""
        update_data = {"name": "Updated Name"}
        response = await async_client.put(
            "/api/v1/teams/999999",
            json=update_data,
            headers=auth_headers
        )
        assert response.status_code == 404

    async def test_delete_nonexistent_team(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test deleting non-existent team returns 404."""
        response = await async_client.delete(
            "/api/v1/teams/999999",
            headers=auth_headers
        )
        assert response.status_code == 404

