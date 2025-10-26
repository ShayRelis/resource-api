"""Dependency injection utilities for the API."""

from typing import AsyncGenerator, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_access_token
from app.crud import user as crud_user
from app.db.database import get_session, get_tenant_session, schema_exists
from app.models import User

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Database session dependency for public schema.
    
    Yields:
        AsyncSession: Database session for public schema
    """
    async for session in get_session():
        yield session


async def get_company_id_from_token(token: str = Depends(oauth2_scheme)) -> int:
    """
    Extract company_id from JWT token.
    
    Args:
        token: JWT token from request
        
    Returns:
        int: Company ID
        
    Raises:
        HTTPException: If token is invalid or company_id missing
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_data = decode_access_token(token)
    if token_data is None or token_data.company_id is None:
        raise credentials_exception
    
    return token_data.company_id


async def get_tenant_db(
    company_id: int = Depends(get_company_id_from_token)
) -> AsyncGenerator[AsyncSession, None]:
    """
    Database session dependency for tenant schema.
    
    Args:
        company_id: Company ID extracted from JWT token
        
    Yields:
        AsyncSession: Database session with search_path set to tenant schema
        
    Raises:
        HTTPException: If company schema doesn't exist
    """
    # Validate schema exists
    if not await schema_exists(company_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company schema not found"
        )
    
    async for session in get_tenant_session(company_id):
        yield session


async def get_current_user(
    db: AsyncSession = Depends(get_tenant_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    """
    Get the current authenticated user from JWT token.
    
    Args:
        db: Tenant database session
        token: JWT token from request
        
    Returns:
        User: Current authenticated user
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_data = decode_access_token(token)
    if token_data is None or token_data.email is None:
        raise credentials_exception
    
    user = await crud_user.get_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Get the current active user.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        User: Current active user
        
    Raises:
        HTTPException: If user is inactive
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user

