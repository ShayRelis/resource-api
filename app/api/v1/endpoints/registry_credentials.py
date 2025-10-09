"""Registry Credential endpoints."""

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user, get_db
from app.crud import registry_credential as crud_registry_credential
from app.models import User
from app.schemas import RegistryCredentialCreate, RegistryCredentialResponse, RegistryCredentialUpdate

router = APIRouter()


@router.post("/", response_model=RegistryCredentialResponse, status_code=status.HTTP_201_CREATED)
async def create_registry_credential(
    registry_credential_in: RegistryCredentialCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create a new registry credential.
    
    Args:
        registry_credential_in: Registry credential creation data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Created registry credential
    """
    registry_credential = await crud_registry_credential.create(db, obj_in=registry_credential_in)
    return registry_credential


@router.get("/", response_model=List[RegistryCredentialResponse])
async def list_registry_credentials(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    List registry credentials with pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        current_user: Current authenticated user
        
    Returns:
        List of registry credentials
    """
    registry_credentials = await crud_registry_credential.get_multi(db, skip=skip, limit=limit)
    return registry_credentials


@router.get("/{registry_credential_id}", response_model=RegistryCredentialResponse)
async def get_registry_credential(
    registry_credential_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get a registry credential by ID.
    
    Args:
        registry_credential_id: Registry credential ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Registry credential instance
        
    Raises:
        HTTPException: If registry credential not found
    """
    registry_credential = await crud_registry_credential.get(db, id=registry_credential_id)
    if not registry_credential:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registry credential not found",
        )
    return registry_credential


@router.put("/{registry_credential_id}", response_model=RegistryCredentialResponse)
async def update_registry_credential(
    registry_credential_id: int,
    registry_credential_in: RegistryCredentialUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update a registry credential.
    
    Args:
        registry_credential_id: Registry credential ID
        registry_credential_in: Registry credential update data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Updated registry credential
        
    Raises:
        HTTPException: If registry credential not found
    """
    registry_credential = await crud_registry_credential.get(db, id=registry_credential_id)
    if not registry_credential:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registry credential not found",
        )
    registry_credential = await crud_registry_credential.update(db, db_obj=registry_credential, obj_in=registry_credential_in)
    return registry_credential


@router.delete("/{registry_credential_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_registry_credential(
    registry_credential_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> None:
    """
    Delete a registry credential.
    
    Args:
        registry_credential_id: Registry credential ID
        db: Database session
        current_user: Current authenticated user
        
    Raises:
        HTTPException: If registry credential not found
    """
    registry_credential = await crud_registry_credential.get(db, id=registry_credential_id)
    if not registry_credential:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registry credential not found",
        )
    await crud_registry_credential.delete(db, id=registry_credential_id)

