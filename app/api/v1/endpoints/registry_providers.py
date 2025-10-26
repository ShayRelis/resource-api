"""Registry Provider endpoints."""

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user, get_tenant_db
from app.crud import registry_provider as crud_registry_provider
from app.models import User
from app.schemas import RegistryProviderCreate, RegistryProviderResponse, RegistryProviderUpdate

router = APIRouter()


@router.post("/", response_model=RegistryProviderResponse, status_code=status.HTTP_201_CREATED)
async def create_registry_provider(
    registry_provider_in: RegistryProviderCreate,
    db: AsyncSession = Depends(get_tenant_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create a new registry provider.
    
    Args:
        registry_provider_in: Registry provider creation data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Created registry provider
    """
    registry_provider = await crud_registry_provider.create(db, obj_in=registry_provider_in)
    return registry_provider


@router.get("/", response_model=List[RegistryProviderResponse])
async def list_registry_providers(
    db: AsyncSession = Depends(get_tenant_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    List registry providers with pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        current_user: Current authenticated user
        
    Returns:
        List of registry providers
    """
    registry_providers = await crud_registry_provider.get_multi(db, skip=skip, limit=limit)
    return registry_providers


@router.get("/{registry_provider_id}", response_model=RegistryProviderResponse)
async def get_registry_provider(
    registry_provider_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get a registry provider by ID.
    
    Args:
        registry_provider_id: Registry provider ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Registry provider instance
        
    Raises:
        HTTPException: If registry provider not found
    """
    registry_provider = await crud_registry_provider.get(db, id=registry_provider_id)
    if not registry_provider:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registry provider not found",
        )
    return registry_provider


@router.put("/{registry_provider_id}", response_model=RegistryProviderResponse)
async def update_registry_provider(
    registry_provider_id: int,
    registry_provider_in: RegistryProviderUpdate,
    db: AsyncSession = Depends(get_tenant_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update a registry provider.
    
    Args:
        registry_provider_id: Registry provider ID
        registry_provider_in: Registry provider update data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Updated registry provider
        
    Raises:
        HTTPException: If registry provider not found
    """
    registry_provider = await crud_registry_provider.get(db, id=registry_provider_id)
    if not registry_provider:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registry provider not found",
        )
    registry_provider = await crud_registry_provider.update(db, db_obj=registry_provider, obj_in=registry_provider_in)
    return registry_provider


@router.delete("/{registry_provider_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_registry_provider(
    registry_provider_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    current_user: User = Depends(get_current_active_user),
) -> None:
    """
    Delete a registry provider.
    
    Args:
        registry_provider_id: Registry provider ID
        db: Database session
        current_user: Current authenticated user
        
    Raises:
        HTTPException: If registry provider not found
    """
    registry_provider = await crud_registry_provider.get(db, id=registry_provider_id)
    if not registry_provider:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registry provider not found",
        )
    await crud_registry_provider.delete(db, id=registry_provider_id)

