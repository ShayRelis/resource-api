"""Team endpoints."""

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.api.deps import get_current_active_user, get_tenant_db
from app.crud import team as crud_team
from app.models import User
from app.schemas import TeamCreate, TeamResponse, TeamUpdate

router = APIRouter()


@router.post("/", response_model=TeamResponse, status_code=status.HTTP_201_CREATED)
async def create_team(
    team_in: TeamCreate,
    db: AsyncSession = Depends(get_tenant_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create a new team.
    
    Args:
        team_in: Team creation data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Created team
        
    Raises:
        HTTPException: If company_id does not exist
    """
    try:
        team = await crud_team.create(db, obj_in=team_in)
        return team
    except IntegrityError as e:
        # Handle foreign key constraint violations
        await db.rollback()
        if "company_id" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company not found",
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database integrity error",
        )


@router.get("/", response_model=List[TeamResponse])
async def list_teams(
    db: AsyncSession = Depends(get_tenant_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    List teams with pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        current_user: Current authenticated user
        
    Returns:
        List of teams
    """
    teams = await crud_team.get_multi(db, skip=skip, limit=limit)
    return teams


@router.get("/{team_id}", response_model=TeamResponse)
async def get_team(
    team_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get a team by ID.
    
    Args:
        team_id: Team ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Team instance
        
    Raises:
        HTTPException: If team not found
    """
    team = await crud_team.get(db, id=team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found",
        )
    return team


@router.put("/{team_id}", response_model=TeamResponse)
async def update_team(
    team_id: int,
    team_in: TeamUpdate,
    db: AsyncSession = Depends(get_tenant_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update a team.
    
    Args:
        team_id: Team ID
        team_in: Team update data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Updated team
        
    Raises:
        HTTPException: If team not found
    """
    team = await crud_team.get(db, id=team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found",
        )
    team = await crud_team.update(db, db_obj=team, obj_in=team_in)
    return team


@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_team(
    team_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    current_user: User = Depends(get_current_active_user),
) -> None:
    """
    Delete a team.
    
    Args:
        team_id: Team ID
        db: Database session
        current_user: Current authenticated user
        
    Raises:
        HTTPException: If team not found
    """
    team = await crud_team.get(db, id=team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found",
        )
    await crud_team.delete(db, id=team_id)

