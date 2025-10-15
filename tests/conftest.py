"""Shared pytest fixtures for all tests."""

import pytest
import httpx
from typing import Dict, AsyncGenerator


@pytest.fixture(scope="session")
def base_url() -> str:
    """Return the base URL for the API."""
    return "http://localhost:8000"


@pytest.fixture
async def async_client(base_url: str) -> AsyncGenerator[httpx.AsyncClient, None]:
    """Create an async HTTP client for testing."""
    async with httpx.AsyncClient(base_url=base_url, timeout=10.0) as client:
        yield client


@pytest.fixture
async def test_user_data() -> Dict[str, str]:
    """Return test user data for registration and login."""
    return {
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "securepassword123",
        "role": "user"
    }


@pytest.fixture
async def auth_token(async_client: httpx.AsyncClient, test_user_data: Dict[str, str]) -> str:
    """Register a test user and return an authentication token."""
    # Try to register the user (might already exist)
    register_response = await async_client.post(
        "/api/v1/auth/register",
        json=test_user_data
    )
    
    # Login to get the token
    login_response = await async_client.post(
        "/api/v1/auth/login",
        data={
            "username": test_user_data["email"],
            "password": test_user_data["password"]
        }
    )
    
    assert login_response.status_code == 200, f"Login failed: {login_response.text}"
    token_data = login_response.json()
    return token_data["access_token"]


@pytest.fixture
async def auth_headers(auth_token: str) -> Dict[str, str]:
    """Return authorization headers with bearer token."""
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture
async def test_company(async_client: httpx.AsyncClient, auth_headers: Dict[str, str]) -> Dict:
    """Create a test company and return its data."""
    company_data = {"name": "Test Company for Fixtures"}
    response = await async_client.post(
        "/api/v1/companies/",
        json=company_data,
        headers=auth_headers
    )
    assert response.status_code == 201
    company = response.json()
    
    yield company
    
    # Cleanup: delete the company after test
    await async_client.delete(
        f"/api/v1/companies/{company['id']}",
        headers=auth_headers
    )


@pytest.fixture
async def test_registry_provider(async_client: httpx.AsyncClient, auth_headers: Dict[str, str]) -> Dict:
    """Create a test registry provider and return its data."""
    provider_data = {"name": "Test Registry Provider"}
    response = await async_client.post(
        "/api/v1/registry-providers/",
        json=provider_data,
        headers=auth_headers
    )
    assert response.status_code == 201
    provider = response.json()
    
    yield provider
    
    # Cleanup: delete the provider after test
    await async_client.delete(
        f"/api/v1/registry-providers/{provider['id']}",
        headers=auth_headers
    )


@pytest.fixture
async def test_registry(
    async_client: httpx.AsyncClient, 
    auth_headers: Dict[str, str],
    test_registry_provider: Dict
) -> Dict:
    """Create a test registry and return its data."""
    registry_data = {
        "name": "Test Registry",
        "url": "https://registry.example.com",
        "is_private": True,
        "registry_provider_id": test_registry_provider["id"]
    }
    response = await async_client.post(
        "/api/v1/registries/",
        json=registry_data,
        headers=auth_headers
    )
    assert response.status_code == 201
    registry = response.json()
    
    yield registry
    
    # Cleanup: delete the registry after test
    await async_client.delete(
        f"/api/v1/registries/{registry['id']}",
        headers=auth_headers
    )

