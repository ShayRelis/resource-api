"""Component endpoints."""

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user, get_db
from app.crud import component as crud_component
from app.models import User
from app.schemas import ComponentCreate, ComponentResponse, ComponentUpdate

router = APIRouter()


@router.post("/", response_model=ComponentResponse, status_code=status.HTTP_201_CREATED)
async def create_component(
    component_in: ComponentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create a new component.
    
    Args:
        component_in: Component creation data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Created component with associations
    """
    component = await crud_component.create_with_associations(db, obj_in=component_in)
    
    # Get associations
    associations = await crud_component.get_associations(db, component_id=component.id)
    
    # Build response
    response_data = {
        "id": component.id,
        "name": component.name,
        "description": component.description,
        "repository_url": component.repository_url,
        "is_managed": component.is_managed,
        "is_third_party": component.is_third_party,
        "company_id": component.company_id,
        "created_at": component.created_at,
        "updated_at": component.updated_at,
        **associations,
    }
    
    return response_data


@router.get("/", response_model=List[ComponentResponse])
async def list_components(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    List components with pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        current_user: Current authenticated user
        
    Returns:
        List of components with their associations
    """
    components = await crud_component.get_multi(db, skip=skip, limit=limit)
    
    # Build response with associations for each component
    response = []
    for component in components:
        associations = await crud_component.get_associations(db, component_id=component.id)
        response_data = {
            "id": component.id,
            "name": component.name,
            "description": component.description,
            "repository_url": component.repository_url,
            "is_managed": component.is_managed,
            "is_third_party": component.is_third_party,
            "company_id": component.company_id,
            "created_at": component.created_at,
            "updated_at": component.updated_at,
            **associations,
        }
        response.append(response_data)
    
    return response


@router.get("/{component_id}", response_model=ComponentResponse)
async def get_component(
    component_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get a component by ID.
    
    Args:
        component_id: Component ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Component instance with associations
        
    Raises:
        HTTPException: If component not found
    """
    component = await crud_component.get(db, id=component_id)
    if not component:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Component not found",
        )
    
    # Get associations
    associations = await crud_component.get_associations(db, component_id=component.id)
    
    # Build response
    response_data = {
        "id": component.id,
        "name": component.name,
        "description": component.description,
        "repository_url": component.repository_url,
        "is_managed": component.is_managed,
        "is_third_party": component.is_third_party,
        "company_id": component.company_id,
        "created_at": component.created_at,
        "updated_at": component.updated_at,
        **associations,
    }
    
    return response_data


@router.put("/{component_id}", response_model=ComponentResponse)
async def update_component(
    component_id: int,
    component_in: ComponentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update a component.
    
    Args:
        component_id: Component ID
        component_in: Component update data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Updated component with associations
        
    Raises:
        HTTPException: If component not found
    """
    component = await crud_component.get(db, id=component_id)
    if not component:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Component not found",
        )
    
    component = await crud_component.update_with_associations(
        db, db_obj=component, obj_in=component_in
    )
    
    # Get associations
    associations = await crud_component.get_associations(db, component_id=component.id)
    
    # Build response
    response_data = {
        "id": component.id,
        "name": component.name,
        "description": component.description,
        "repository_url": component.repository_url,
        "is_managed": component.is_managed,
        "is_third_party": component.is_third_party,
        "company_id": component.company_id,
        "created_at": component.created_at,
        "updated_at": component.updated_at,
        **associations,
    }
    
    return response_data


@router.delete("/{component_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_component(
    component_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> None:
    """
    Delete a component.
    
    Args:
        component_id: Component ID
        db: Database session
        current_user: Current authenticated user
        
    Raises:
        HTTPException: If component not found
    """
    component = await crud_component.get(db, id=component_id)
    if not component:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Component not found",
        )
    
    await crud_component.delete_with_associations(db, id=component_id)

