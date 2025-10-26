"""Environment endpoints."""

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user, get_db
from app.crud import environment as crud_environment
from app.models import User
from app.schemas.environment import EnvironmentCreate, EnvironmentResponse, EnvironmentUpdate

router = APIRouter()


@router.post("/", response_model=EnvironmentResponse, status_code=status.HTTP_201_CREATED)
async def create_environment(
    environment_in: EnvironmentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create a new environment.
    
    Args:
        environment_in: Environment creation data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Created environment
    """
    environment = await crud_environment.create(db, obj_in=environment_in)
    return environment


@router.get("/", response_model=List[EnvironmentResponse])
async def list_environments(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    List environments with pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        current_user: Current authenticated user
        
    Returns:
        List of environments
    """
    environments = await crud_environment.get_multi(db, skip=skip, limit=limit)
    return environments


@router.get("/{environment_id}", response_model=EnvironmentResponse)
async def get_environment(
    environment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get an environment by ID.
    
    Args:
        environment_id: Environment ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Environment instance
        
    Raises:
        HTTPException: If environment not found
    """
    environment = await crud_environment.get(db, id=environment_id)
    if not environment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Environment not found",
        )
    return environment


@router.put("/{environment_id}", response_model=EnvironmentResponse)
async def update_environment(
    environment_id: int,
    environment_in: EnvironmentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update an environment.
    
    Args:
        environment_id: Environment ID
        environment_in: Environment update data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Updated environment
        
    Raises:
        HTTPException: If environment not found
    """
    environment = await crud_environment.get(db, id=environment_id)
    if not environment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Environment not found",
        )
    environment = await crud_environment.update(db, db_obj=environment, obj_in=environment_in)
    return environment


@router.delete("/{environment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_environment(
    environment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> None:
    """
    Delete an environment.
    
    Args:
        environment_id: Environment ID
        db: Database session
        current_user: Current authenticated user
        
    Raises:
        HTTPException: If environment not found
    """
    environment = await crud_environment.get(db, id=environment_id)
    if not environment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Environment not found",
        )
    await crud_environment.delete(db, id=environment_id)

