"""Registry endpoints."""

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user, get_db
from app.crud import registry as crud_registry
from app.models import User
from app.schemas import RegistryCreate, RegistryResponse, RegistryUpdate

router = APIRouter()


@router.post("/", response_model=RegistryResponse, status_code=status.HTTP_201_CREATED)
async def create_registry(
    registry_in: RegistryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create a new registry.
    
    Args:
        registry_in: Registry creation data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Created registry
    """
    registry = await crud_registry.create(db, obj_in=registry_in)
    return registry


@router.get("/", response_model=List[RegistryResponse])
async def list_registries(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    List registries with pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        current_user: Current authenticated user
        
    Returns:
        List of registries
    """
    registries = await crud_registry.get_multi(db, skip=skip, limit=limit)
    return registries


@router.get("/{registry_id}", response_model=RegistryResponse)
async def get_registry(
    registry_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get a registry by ID.
    
    Args:
        registry_id: Registry ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Registry instance
        
    Raises:
        HTTPException: If registry not found
    """
    registry = await crud_registry.get(db, id=registry_id)
    if not registry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registry not found",
        )
    return registry


@router.put("/{registry_id}", response_model=RegistryResponse)
async def update_registry(
    registry_id: int,
    registry_in: RegistryUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update a registry.
    
    Args:
        registry_id: Registry ID
        registry_in: Registry update data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Updated registry
        
    Raises:
        HTTPException: If registry not found
    """
    registry = await crud_registry.get(db, id=registry_id)
    if not registry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registry not found",
        )
    registry = await crud_registry.update(db, db_obj=registry, obj_in=registry_in)
    return registry


@router.delete("/{registry_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_registry(
    registry_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> None:
    """
    Delete a registry.
    
    Args:
        registry_id: Registry ID
        db: Database session
        current_user: Current authenticated user
        
    Raises:
        HTTPException: If registry not found
    """
    registry = await crud_registry.get(db, id=registry_id)
    if not registry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registry not found",
        )
    await crud_registry.delete(db, id=registry_id)

