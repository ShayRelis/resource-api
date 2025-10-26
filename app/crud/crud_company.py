"""CRUD operations for Company model."""

from fastapi import HTTPException, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.crud.crud_user_company_lookup import user_company_lookup as crud_lookup
from app.db.database import create_company_schema, get_schema_name, engine
from app.models import Company
from app.schemas import CompanyCreate, CompanyUpdate


class CRUDCompany(CRUDBase[Company, CompanyCreate, CompanyUpdate]):
    """CRUD operations for Company model."""

    async def create(self, db: AsyncSession, *, obj_in: CompanyCreate) -> Company:
        """
        Create a new company and its tenant schema.
        
        Args:
            db: Database session
            obj_in: Company creation data
            
        Returns:
            Created company instance
        """
        # Create company record in public schema
        db_obj = Company(name=obj_in.name)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        
        # Create tenant schema and seed reference data
        try:
            await create_company_schema(db_obj.id, seed_data=True)
        except Exception as e:
            # If schema creation fails, rollback company creation
            await db.delete(db_obj)
            await db.commit()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create company schema: {str(e)}"
            )
        
        return db_obj

    async def delete(self, db: AsyncSession, *, id: int) -> Company:
        """
        Delete a company and its tenant schema.
        
        Args:
            db: Database session
            id: Company ID
            
        Returns:
            Deleted company instance
            
        Raises:
            HTTPException: If company has users or doesn't exist
        """
        # Get company
        company = await self.get(db, id=id)
        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company not found"
            )
        
        # Check if company has users
        user_count = await crud_lookup.count_by_company(db, company_id=id)
        if user_count > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot delete company with {user_count} existing users"
            )
        
        # Drop tenant schema
        schema_name = get_schema_name(id)
        async with engine.begin() as conn:
            await conn.execute(text(f"DROP SCHEMA IF EXISTS {schema_name} CASCADE"))
        
        # Delete company record (cascade will handle user_company_lookup)
        await db.delete(company)
        await db.commit()
        
        return company


# Create instance
company = CRUDCompany(Company)

