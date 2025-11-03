from typing import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import get_settings

settings = get_settings()

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
    future=True,
    pool_size=5,
    max_overflow=10
)

async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Separate base classes for public and tenant schemas
class PublicBase(DeclarativeBase):
    """Base class for tables in public schema (companies, user_company_lookup)"""
    pass

class TenantBase(DeclarativeBase):
    """Base class for tables in tenant schemas (all company-specific data)"""
    pass

# Keep Base for backward compatibility during migration
Base = PublicBase


def get_schema_name(company_id: int) -> str:
    """
    Get the schema name for a company with validation to prevent SQL injection.
    
    Args:
        company_id: The company ID
        
    Returns:
        The schema name (e.g., "company_1")
        
    Raises:
        ValueError: If company_id is invalid
    """
    if not isinstance(company_id, int) or company_id <= 0:
        raise ValueError(f"Invalid company_id: {company_id}")
    return f"company_{company_id}"


async def schema_exists(company_id: int) -> bool:
    """
    Check if a company schema exists.
    
    Args:
        company_id: The company ID
        
    Returns:
        True if schema exists, False otherwise
    """
    schema_name = get_schema_name(company_id)
    async with engine.begin() as conn:
        result = await conn.execute(
            text("SELECT schema_name FROM information_schema.schemata WHERE schema_name = :name"),
            {"name": schema_name}
        )
        return result.scalar() is not None


async def create_company_schema(company_id: int, seed_data: bool = True) -> None:
    """
    Create a new company schema and all tenant tables.
    
    Args:
        company_id: The company ID
        seed_data: Whether to seed reference data (default: True)
    """
    from app.seed.seed_reference_data import seed_tenant_reference_data
    
    schema_name = get_schema_name(company_id)
    
    # Create schema
    async with engine.begin() as conn:
        await conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema_name}"))
    
    # Create tables in the schema
    async with engine.begin() as conn:
        def _create_tables(sync_conn):
            sync_conn.execute(text(f"SET search_path TO {schema_name}"))
            TenantBase.metadata.create_all(bind=sync_conn)
        await conn.run_sync(_create_tables)
    
    # Seed reference data
    if seed_data:
        async for session in get_tenant_session(company_id):
            await seed_tenant_reference_data(session, company_id)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Get a database session for public schema access.
    
    Yields:
        AsyncSession for public schema
    """
    async with async_session() as session:
        try:
            # Explicitly set search_path to public schema
            await session.execute(text("SET search_path TO public"))
            yield session
        finally:
            await session.close()


async def get_tenant_session(company_id: int) -> AsyncGenerator[AsyncSession, None]:
    """
    Get a database session with search_path set to company schema.
    
    Args:
        company_id: The company ID
        
    Yields:
        AsyncSession with search_path set to tenant schema
    """
    schema_name = get_schema_name(company_id)
    async with async_session() as session:
        try:
            # Set search path to tenant schema
            await session.execute(text(f"SET search_path TO {schema_name}"))
            yield session
        finally:
            await session.close() 