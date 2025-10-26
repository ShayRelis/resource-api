import asyncio
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy.ext.asyncio import create_async_engine

import app.models  # noqa: F401 - ensure models are registered with Base
from app.core.config import get_settings
from app.db.database import PublicBase, TenantBase

async def create_public_tables():
    """Create public schema tables (companies, user_company_lookup)."""
    settings = get_settings()
    
    # Create async engine
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=True,
        future=True
    )
    
    async with engine.begin() as conn:
        # Create all public schema tables
        await conn.run_sync(PublicBase.metadata.create_all)
        print("✓ Public schema tables created successfully!")

async def create_tenant_schema_tables(company_id: int):
    """
    Create tenant schema tables for a specific company.
    
    This is typically called automatically when a company is created,
    but can be used manually for migrations or testing.
    """
    from app.db.database import create_company_schema
    
    await create_company_schema(company_id, seed_data=True)
    print(f"✓ Tenant schema for company_{company_id} created successfully!")

if __name__ == "__main__":
    print("Creating public schema tables...")
    asyncio.run(create_public_tables())
    print("\nNote: Tenant schemas are created automatically when companies are created.")
    print("To manually create a tenant schema, use:")
    print("  python -c 'from app.db.create_tables import create_tenant_schema_tables; import asyncio; asyncio.run(create_tenant_schema_tables(1))'") 