"""User endpoints."""

import logging
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user, get_tenant_db, get_db, get_company_id_from_token
from app.crud import user as crud_user
from app.crud.crud_user_company_lookup import user_company_lookup as crud_lookup
from app.models import User
from app.schemas import UserCreate, UserResponse, UserUpdate

logger = logging.getLogger(__name__)

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
    logger.info(f"Attempting to create user with email: {user_in.email} for company_id: {company_id}")
    
    # Check if email already exists in lookup table (across all companies)
    existing_lookup = await crud_lookup.get_by_email(public_db, email=user_in.email)
    if existing_lookup:
        logger.warning(f"User creation failed: Email {user_in.email} already registered")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    # Check if user exists in current tenant schema (extra safety)
    user = await crud_user.get_by_email(db, email=user_in.email)
    if user:
        logger.warning(f"User creation failed: Email {user_in.email} already exists in tenant schema")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    # Create user in tenant schema
    user = await crud_user.create(db, obj_in=user_in)
    logger.info(f"User created in tenant schema: {user.email} (id: {user.id})")
    
    # Create lookup entry in public schema with error handling and rollback
    try:
        await crud_lookup.create_entry(public_db, email=user.email, company_id=company_id)
        logger.info(f"User company lookup entry created: {user.email} -> company_id: {company_id}")
    except Exception as e:
        logger.error(f"Failed to create lookup entry for {user.email}. Rolling back user creation. Error: {str(e)}")
        # Rollback: Delete the user from tenant schema
        try:
            await crud_user.delete(db, id=user.id)
            logger.info(f"Successfully rolled back user creation for {user.email}")
        except Exception as rollback_error:
            logger.critical(f"CRITICAL: Failed to rollback user creation for {user.email}. Error: {str(rollback_error)}")
        
        # Raise error to client
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user lookup entry: {str(e)}",
        )
    
    logger.info(f"User creation completed successfully: {user.email}")
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
        logger.warning(f"User deletion failed: User {user_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    logger.info(f"Deleting user: {user.email} (id: {user_id})")
    
    # Delete user from tenant schema
    await crud_user.delete(db, id=user_id)
    logger.info(f"User deleted from tenant schema: {user.email}")
    
    # Delete lookup entry from public schema
    deleted = await crud_lookup.delete_by_email(public_db, email=user.email)
    if deleted:
        logger.info(f"User company lookup entry deleted: {user.email}")
    else:
        logger.warning(f"No lookup entry found to delete for user: {user.email}")

