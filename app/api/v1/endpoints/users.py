"""User endpoints."""

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user, get_tenant_db, get_db, get_company_id_from_token
from app.crud import user as crud_user
from app.crud.crud_user_company_lookup import user_company_lookup as crud_lookup
from app.models import User
from app.schemas import UserCreate, UserResponse, UserUpdate

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_tenant_db),
    public_db: AsyncSession = Depends(get_db),
    company_id: int = Depends(get_company_id_from_token),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create a new user.
    
    Args:
        user_in: User creation data
        db: Tenant database session
        public_db: Public database session
        company_id: Company ID from authentication token
        current_user: Current authenticated user
        
    Returns:
        Created user
        
    Raises:
        HTTPException: If email already registered
    """
    # Check if email already exists in lookup table (across all companies)
    existing_lookup = await crud_lookup.get_by_email(public_db, email=user_in.email)
    if existing_lookup:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    # Check if user exists in current tenant schema (extra safety)
    user = await crud_user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    # Create user in tenant schema
    user = await crud_user.create(db, obj_in=user_in)
    
    # Create lookup entry in public schema
    await crud_lookup.create_entry(public_db, email=user.email, company_id=company_id)
    
    return user


@router.get("/", response_model=List[UserResponse])
async def list_users(
    db: AsyncSession = Depends(get_tenant_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    List users with pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        current_user: Current authenticated user
        
    Returns:
        List of users
    """
    users = await crud_user.get_multi(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get a user by ID.
    
    Args:
        user_id: User ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        User instance
        
    Raises:
        HTTPException: If user not found
    """
    user = await crud_user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: AsyncSession = Depends(get_tenant_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update a user.
    
    Args:
        user_id: User ID
        user_in: User update data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Updated user
        
    Raises:
        HTTPException: If user not found
    """
    user = await crud_user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    user = await crud_user.update(db, db_obj=user, obj_in=user_in)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    public_db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> None:
    """
    Delete a user.
    
    Args:
        user_id: User ID
        db: Tenant database session
        public_db: Public database session
        current_user: Current authenticated user
        
    Raises:
        HTTPException: If user not found
    """
    user = await crud_user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    # Delete user from tenant schema
    await crud_user.delete(db, id=user_id)
    
    # Delete lookup entry from public schema
    await crud_lookup.delete_by_email(public_db, email=user.email)

