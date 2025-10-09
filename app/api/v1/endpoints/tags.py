"""Tag endpoints."""

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user, get_db
from app.crud import tag as crud_tag
from app.models import User
from app.schemas import TagCreate, TagResponse, TagUpdate

router = APIRouter()


@router.post("/", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
async def create_tag(
    tag_in: TagCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create a new tag.
    
    Args:
        tag_in: Tag creation data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Created tag
    """
    tag = await crud_tag.create(db, obj_in=tag_in)
    return tag


@router.get("/", response_model=List[TagResponse])
async def list_tags(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    List tags with pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        current_user: Current authenticated user
        
    Returns:
        List of tags
    """
    tags = await crud_tag.get_multi(db, skip=skip, limit=limit)
    return tags


@router.get("/{tag_id}", response_model=TagResponse)
async def get_tag(
    tag_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get a tag by ID.
    
    Args:
        tag_id: Tag ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Tag instance
        
    Raises:
        HTTPException: If tag not found
    """
    tag = await crud_tag.get(db, id=tag_id)
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found",
        )
    return tag


@router.put("/{tag_id}", response_model=TagResponse)
async def update_tag(
    tag_id: int,
    tag_in: TagUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update a tag.
    
    Args:
        tag_id: Tag ID
        tag_in: Tag update data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Updated tag
        
    Raises:
        HTTPException: If tag not found
    """
    tag = await crud_tag.get(db, id=tag_id)
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found",
        )
    tag = await crud_tag.update(db, db_obj=tag, obj_in=tag_in)
    return tag


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(
    tag_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> None:
    """
    Delete a tag.
    
    Args:
        tag_id: Tag ID
        db: Database session
        current_user: Current authenticated user
        
    Raises:
        HTTPException: If tag not found
    """
    tag = await crud_tag.get(db, id=tag_id)
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found",
        )
    await crud_tag.delete(db, id=tag_id)

