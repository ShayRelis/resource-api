"""Container Image endpoints."""

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.api.deps import get_current_active_user, get_tenant_db
from app.crud import container_image as crud_container_image
from app.models import User
from app.schemas import ContainerImageCreate, ContainerImageResponse, ContainerImageUpdate

router = APIRouter()


@router.post("/", response_model=ContainerImageResponse, status_code=status.HTTP_201_CREATED)
async def create_container_image(
    container_image_in: ContainerImageCreate,
    db: AsyncSession = Depends(get_tenant_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create a new container image.
    
    Args:
        container_image_in: Container image creation data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Created container image
        
    Raises:
        HTTPException: If registry_id does not exist
    """
    try:
        container_image = await crud_container_image.create(db, obj_in=container_image_in)
        return container_image
    except IntegrityError as e:
        # Handle foreign key constraint violations
        await db.rollback()
        if "registry_id" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registry not found",
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database integrity error",
        )


@router.get("/", response_model=List[ContainerImageResponse])
async def list_container_images(
    db: AsyncSession = Depends(get_tenant_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    List container images with pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        current_user: Current authenticated user
        
    Returns:
        List of container images
    """
    container_images = await crud_container_image.get_multi(db, skip=skip, limit=limit)
    return container_images


@router.get("/{container_image_id}", response_model=ContainerImageResponse)
async def get_container_image(
    container_image_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get a container image by ID.
    
    Args:
        container_image_id: Container image ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Container image instance
        
    Raises:
        HTTPException: If container image not found
    """
    container_image = await crud_container_image.get(db, id=container_image_id)
    if not container_image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Container image not found",
        )
    return container_image


@router.put("/{container_image_id}", response_model=ContainerImageResponse)
async def update_container_image(
    container_image_id: int,
    container_image_in: ContainerImageUpdate,
    db: AsyncSession = Depends(get_tenant_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update a container image.
    
    Args:
        container_image_id: Container image ID
        container_image_in: Container image update data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Updated container image
        
    Raises:
        HTTPException: If container image not found
    """
    container_image = await crud_container_image.get(db, id=container_image_id)
    if not container_image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Container image not found",
        )
    container_image = await crud_container_image.update(db, db_obj=container_image, obj_in=container_image_in)
    return container_image


@router.delete("/{container_image_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_container_image(
    container_image_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    current_user: User = Depends(get_current_active_user),
) -> None:
    """
    Delete a container image.
    
    Args:
        container_image_id: Container image ID
        db: Database session
        current_user: Current authenticated user
        
    Raises:
        HTTPException: If container image not found
    """
    container_image = await crud_container_image.get(db, id=container_image_id)
    if not container_image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Container image not found",
        )
    await crud_container_image.delete(db, id=container_image_id)

