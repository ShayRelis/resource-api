"""CRUD operations for UserCompanyLookup model."""

from typing import Optional, List

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.user_company_lookup import UserCompanyLookup
from pydantic import BaseModel


class UserCompanyLookupCreate(BaseModel):
    """Schema for creating user company lookup entry."""
    email: str
    company_id: int


class UserCompanyLookupUpdate(BaseModel):
    """Schema for updating user company lookup entry."""
    company_id: Optional[int] = None


class CRUDUserCompanyLookup(CRUDBase[UserCompanyLookup, UserCompanyLookupCreate, UserCompanyLookupUpdate]):
    """CRUD operations for UserCompanyLookup model."""

    async def get_by_email(self, db: AsyncSession, *, email: str) -> Optional[UserCompanyLookup]:
        """
        Get a user company lookup entry by email.
        
        Args:
            db: Database session
            email: User email address
            
        Returns:
            UserCompanyLookup instance if found, None otherwise
        """
        result = await db.execute(select(UserCompanyLookup).filter(UserCompanyLookup.email == email))
        return result.scalar_one_or_none()

    async def get_by_company_id(self, db: AsyncSession, *, company_id: int) -> List[UserCompanyLookup]:
        """
        Get all user company lookup entries for a company.
        
        Args:
            db: Database session
            company_id: Company ID
            
        Returns:
            List of UserCompanyLookup instances
        """
        result = await db.execute(
            select(UserCompanyLookup).filter(UserCompanyLookup.company_id == company_id)
        )
        return list(result.scalars().all())

    async def count_by_company(self, db: AsyncSession, *, company_id: int) -> int:
        """
        Count the number of users in a company.
        
        Args:
            db: Database session
            company_id: Company ID
            
        Returns:
            Number of users in the company
        """
        result = await db.execute(
            select(func.count()).select_from(UserCompanyLookup).filter(
                UserCompanyLookup.company_id == company_id
            )
        )
        return result.scalar() or 0

    async def delete_by_email(self, db: AsyncSession, *, email: str) -> bool:
        """
        Delete a user company lookup entry by email.
        
        Args:
            db: Database session
            email: User email address
            
        Returns:
            True if deleted, False if not found
        """
        lookup = await self.get_by_email(db, email=email)
        if lookup:
            await db.delete(lookup)
            await db.commit()
            return True
        return False

    async def create_entry(
        self, db: AsyncSession, *, email: str, company_id: int
    ) -> UserCompanyLookup:
        """
        Create a new user company lookup entry.
        
        Args:
            db: Database session
            email: User email
            company_id: Company ID
            
        Returns:
            Created UserCompanyLookup instance
        """
        db_obj = UserCompanyLookup(email=email, company_id=company_id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


# Create instance
user_company_lookup = CRUDUserCompanyLookup(UserCompanyLookup)

