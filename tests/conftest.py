"""Shared pytest fixtures for all tests."""

import pytest
import httpx
from typing import Dict, AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncConnection
from sqlalchemy.orm import sessionmaker

from main import app
from app.api.deps import get_db
from app.core.config import get_settings


settings = get_settings()


@pytest.fixture(scope="session")
def base_url() -> str:
    """Return the base URL for the API."""
    return "http://localhost:8000"


@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Create a database session with automatic rollback for testing."""
    from sqlalchemy.pool import NullPool
    
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=False,
        future=True,
        poolclass=NullPool,
        connect_args={"statement_cache_size": 0},
    )
    
    async with engine.connect() as connection:
        transaction = await connection.begin()
        
        async_session_factory = sessionmaker(
            connection,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
        )
        
        async with async_session_factory() as session:
            yield session
            await session.close()
        
        await transaction.rollback()
    
    await engine.dispose()


@pytest.fixture
async def async_client(db_session: AsyncSession) -> AsyncGenerator[httpx.AsyncClient, None]:
    """Create an async HTTP client for testing with database dependency override."""
    async def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    # Use the app directly with ASGI transport instead of external HTTP server
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test",
        timeout=10.0
    ) as client:
        yield client
    
    app.dependency_overrides.clear()


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
async def test_company_id(db_session: AsyncSession) -> int:
    """Create a test company and return its ID."""
    from app.models.company import Company
    from app.db.database import create_company_schema
    
    # Create company in public schema
    company = Company(name="Test Company")
    db_session.add(company)
    await db_session.commit()
    await db_session.refresh(company)
    
    # Create tenant schema for the company
    await create_company_schema(company.id, seed_data=True)
    
    return company.id


@pytest.fixture
async def test_user(db_session: AsyncSession, test_user_data: Dict[str, str], test_company_id: int) -> Dict:
    """Create a test user in the tenant schema and return user data with company_id."""
    from app.models.user import User, UserRole
    from app.models.user_company_lookup import UserCompanyLookup
    from app.core.security import get_password_hash
    from app.db.database import get_tenant_session
    
    # Create user in tenant schema
    async for tenant_session in get_tenant_session(test_company_id):
        user = User(
            name=test_user_data["name"],
            email=test_user_data["email"],
            password_hash=get_password_hash(test_user_data["password"]),
            role=UserRole[test_user_data["role"]],
            is_active=True
        )
        tenant_session.add(user)
        await tenant_session.commit()
        await tenant_session.refresh(user)
    
    # Create user_company_lookup entry in public schema
    lookup = UserCompanyLookup(
        email=test_user_data["email"],
        company_id=test_company_id
    )
    db_session.add(lookup)
    await db_session.commit()
    
    return {**test_user_data, "company_id": test_company_id}


@pytest.fixture
async def auth_token(async_client: httpx.AsyncClient, test_user: Dict[str, str]) -> str:
    """Login with test user and return an authentication token."""
    # Login to get the token
    login_response = await async_client.post(
        "/api/v1/auth/login",
        data={
            "username": test_user["email"],
            "password": test_user["password"]
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
    return response.json()


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
    return response.json()


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
    return response.json()


@pytest.fixture
async def test_version(async_client: httpx.AsyncClient, auth_headers: Dict[str, str]) -> Dict:
    """Create a test version and return its data."""
    version_data = {"name": "Test Version v1.0.0"}
    response = await async_client.post(
        "/api/v1/versions/",
        json=version_data,
        headers=auth_headers
    )
    assert response.status_code == 201
    return response.json()

