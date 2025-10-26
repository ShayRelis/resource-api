"""Cloud Provider endpoints."""

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user, get_tenant_db
from app.crud import cloud_provider as crud_cloud_provider
from app.models import User
from app.schemas import CloudProviderCreate, CloudProviderResponse, CloudProviderUpdate

router = APIRouter()


@router.post("/", response_model=CloudProviderResponse, status_code=status.HTTP_201_CREATED)
async def create_cloud_provider(
    cloud_provider_in: CloudProviderCreate,
    db: AsyncSession = Depends(get_tenant_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create a new cloud provider.
    
    Args:
        cloud_provider_in: Cloud provider creation data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Created cloud provider
    """
    cloud_provider = await crud_cloud_provider.create(db, obj_in=cloud_provider_in)
    return cloud_provider


@router.get("/", response_model=List[CloudProviderResponse])
async def list_cloud_providers(
    db: AsyncSession = Depends(get_tenant_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    List cloud providers with pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        current_user: Current authenticated user
        
    Returns:
        List of cloud providers
    """
    cloud_providers = await crud_cloud_provider.get_multi(db, skip=skip, limit=limit)
    return cloud_providers


@router.get("/{cloud_provider_id}", response_model=CloudProviderResponse)
async def get_cloud_provider(
    cloud_provider_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get a cloud provider by ID.
    
    Args:
        cloud_provider_id: Cloud provider ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Cloud provider instance
        
    Raises:
        HTTPException: If cloud provider not found
    """
    cloud_provider = await crud_cloud_provider.get(db, id=cloud_provider_id)
    if not cloud_provider:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cloud provider not found",
        )
    return cloud_provider


@router.put("/{cloud_provider_id}", response_model=CloudProviderResponse)
async def update_cloud_provider(
    cloud_provider_id: int,
    cloud_provider_in: CloudProviderUpdate,
    db: AsyncSession = Depends(get_tenant_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update a cloud provider.
    
    Args:
        cloud_provider_id: Cloud provider ID
        cloud_provider_in: Cloud provider update data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Updated cloud provider
        
    Raises:
        HTTPException: If cloud provider not found
    """
    cloud_provider = await crud_cloud_provider.get(db, id=cloud_provider_id)
    if not cloud_provider:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cloud provider not found",
        )
    cloud_provider = await crud_cloud_provider.update(db, db_obj=cloud_provider, obj_in=cloud_provider_in)
    return cloud_provider


@router.delete("/{cloud_provider_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cloud_provider(
    cloud_provider_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    current_user: User = Depends(get_current_active_user),
) -> None:
    """
    Delete a cloud provider.
    
    Args:
        cloud_provider_id: Cloud provider ID
        db: Database session
        current_user: Current authenticated user
        
    Raises:
        HTTPException: If cloud provider not found
    """
    cloud_provider = await crud_cloud_provider.get(db, id=cloud_provider_id)
    if not cloud_provider:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cloud provider not found",
        )
    await crud_cloud_provider.delete(db, id=cloud_provider_id)

