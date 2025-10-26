"""Version endpoints."""

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user, get_tenant_db
from app.crud import version as crud_version
from app.models import User
from app.schemas import VersionCreate, VersionResponse, VersionUpdate

router = APIRouter()


@router.post("/", response_model=VersionResponse, status_code=status.HTTP_201_CREATED)
async def create_version(
    version_in: VersionCreate,
    db: AsyncSession = Depends(get_tenant_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create a new version.
    
    Args:
        version_in: Version creation data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Created version
    """
    version = await crud_version.create(db, obj_in=version_in)
    return version


@router.get("/", response_model=List[VersionResponse])
async def list_versions(
    db: AsyncSession = Depends(get_tenant_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    List versions with pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        current_user: Current authenticated user
        
    Returns:
        List of versions
    """
    versions = await crud_version.get_multi(db, skip=skip, limit=limit)
    return versions


@router.get("/{version_id}", response_model=VersionResponse)
async def get_version(
    version_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get a version by ID.
    
    Args:
        version_id: Version ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Version instance
        
    Raises:
        HTTPException: If version not found
    """
    version = await crud_version.get(db, id=version_id)
    if not version:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Version not found",
        )
    return version


@router.put("/{version_id}", response_model=VersionResponse)
async def update_version(
    version_id: int,
    version_in: VersionUpdate,
    db: AsyncSession = Depends(get_tenant_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update a version.
    
    Args:
        version_id: Version ID
        version_in: Version update data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Updated version
        
    Raises:
        HTTPException: If version not found
    """
    version = await crud_version.get(db, id=version_id)
    if not version:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Version not found",
        )
    version = await crud_version.update(db, db_obj=version, obj_in=version_in)
    return version


@router.delete("/{version_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_version(
    version_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    current_user: User = Depends(get_current_active_user),
) -> None:
    """
    Delete a version.
    
    Args:
        version_id: Version ID
        db: Database session
        current_user: Current authenticated user
        
    Raises:
        HTTPException: If version not found
    """
    version = await crud_version.get(db, id=version_id)
    if not version:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Version not found",
        )
    await crud_version.delete(db, id=version_id)

