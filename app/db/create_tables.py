import asyncio
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy.ext.asyncio import create_async_engine

import app.models  # noqa: F401 - ensure models are registered with Base
from app.core.config import get_settings
from app.db.database import Base

async def create_tables():
    settings = get_settings()
    
    # Create async engine
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=True,
        future=True
    )
    
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
        print("All tables created successfully!")

if __name__ == "__main__":
    asyncio.run(create_tables()) 