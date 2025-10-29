"""CRUD operations for User model."""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models import User
from app.schemas import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """CRUD operations for User model."""

    async def get_by_email(self, db: AsyncSession, *, email: str) -> Optional[User]:
        """
        Get a user by email.
        
        Args:
            db: Database session
            email: User email address
            
        Returns:
            User instance if found, None otherwise
        """
        result = await db.execute(select(User).filter(User.email == email))
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, *, obj_in: UserCreate) -> User:
        """
        Create a new user with hashed password.
        
        Args:
            db: Database session
            obj_in: User creation schema
            
        Returns:
            Created user instance
        """
        db_obj = User(
            name=obj_in.name,
            email=obj_in.email,
            phone=obj_in.phone,
            password_hash=get_password_hash(obj_in.password),
            role=obj_in.role,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def authenticate(
        self, db: AsyncSession, *, email: str, password: str
    ) -> Optional[User]:
        """
        Authenticate a user by email and password.
        
        Args:
            db: Database session
            email: User email address
            password: Plain text password
            
        Returns:
            User instance if authentication successful, None otherwise
        """
        user = await self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    async def is_active(self, user: User) -> bool:
        """
        Check if user is active.
        
        Args:
            user: User instance
            
        Returns:
            True if user is active, False otherwise
        """
        return user.is_active


# Create instance
user = CRUDUser(User)

