"""Service Type endpoints."""

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user, get_tenant_db
from app.crud import service_type as crud_service_type
from app.models import User
from app.schemas import ServiceTypeCreate, ServiceTypeResponse, ServiceTypeUpdate

router = APIRouter()


@router.post("/", response_model=ServiceTypeResponse, status_code=status.HTTP_201_CREATED)
async def create_service_type(
    service_type_in: ServiceTypeCreate,
    db: AsyncSession = Depends(get_tenant_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create a new service type.
    
    Args:
        service_type_in: Service type creation data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Created service type
    """
    service_type = await crud_service_type.create(db, obj_in=service_type_in)
    return service_type


@router.get("/", response_model=List[ServiceTypeResponse])
async def list_service_types(
    db: AsyncSession = Depends(get_tenant_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    List service types with pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        current_user: Current authenticated user
        
    Returns:
        List of service types
    """
    service_types = await crud_service_type.get_multi(db, skip=skip, limit=limit)
    return service_types


@router.get("/{service_type_id}", response_model=ServiceTypeResponse)
async def get_service_type(
    service_type_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get a service type by ID.
    
    Args:
        service_type_id: Service type ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Service type instance
        
    Raises:
        HTTPException: If service type not found
    """
    service_type = await crud_service_type.get(db, id=service_type_id)
    if not service_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service type not found",
        )
    return service_type


@router.put("/{service_type_id}", response_model=ServiceTypeResponse)
async def update_service_type(
    service_type_id: int,
    service_type_in: ServiceTypeUpdate,
    db: AsyncSession = Depends(get_tenant_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update a service type.
    
    Args:
        service_type_id: Service type ID
        service_type_in: Service type update data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Updated service type
        
    Raises:
        HTTPException: If service type not found
    """
    service_type = await crud_service_type.get(db, id=service_type_id)
    if not service_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service type not found",
        )
    service_type = await crud_service_type.update(db, db_obj=service_type, obj_in=service_type_in)
    return service_type


@router.delete("/{service_type_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_service_type(
    service_type_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    current_user: User = Depends(get_current_active_user),
) -> None:
    """
    Delete a service type.
    
    Args:
        service_type_id: Service type ID
        db: Database session
        current_user: Current authenticated user
        
    Raises:
        HTTPException: If service type not found
    """
    service_type = await crud_service_type.get(db, id=service_type_id)
    if not service_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service type not found",
        )
    await crud_service_type.delete(db, id=service_type_id)

