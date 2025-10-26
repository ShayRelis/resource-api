"""Company endpoints."""

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user, get_db
from app.crud import company as crud_company
from app.models import User
from app.schemas import CompanyCreate, CompanyResponse, CompanyUpdate

router = APIRouter()


@router.post("/", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
async def create_company(
    company_in: CompanyCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create a new company. Requires admin role.
    
    Args:
        company_in: Company creation data
        db: Database session
        current_user: Current authenticated user (must be admin)
        
    Returns:
        Created company
        
    Raises:
        HTTPException: If user is not an admin
    """
    # Check if user is admin
    from app.models.user import UserRole
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can create companies"
        )
    
    company = await crud_company.create(db, obj_in=company_in)
    return company


@router.get("/", response_model=List[CompanyResponse])
async def list_companies(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    List companies with pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        current_user: Current authenticated user
        
    Returns:
        List of companies
    """
    companies = await crud_company.get_multi(db, skip=skip, limit=limit)
    return companies


@router.get("/{company_id}", response_model=CompanyResponse)
async def get_company(
    company_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get a company by ID.
    
    Args:
        company_id: Company ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Company instance
        
    Raises:
        HTTPException: If company not found
    """
    company = await crud_company.get(db, id=company_id)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found",
        )
    return company


@router.put("/{company_id}", response_model=CompanyResponse)
async def update_company(
    company_id: int,
    company_in: CompanyUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update a company.
    
    Args:
        company_id: Company ID
        company_in: Company update data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Updated company
        
    Raises:
        HTTPException: If company not found
    """
    company = await crud_company.get(db, id=company_id)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found",
        )
    company = await crud_company.update(db, db_obj=company, obj_in=company_in)
    return company


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(
    company_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> None:
    """
    Delete a company.
    
    Args:
        company_id: Company ID
        db: Database session
        current_user: Current authenticated user
        
    Raises:
        HTTPException: If company not found
    """
    company = await crud_company.get(db, id=company_id)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found",
        )
    await crud_company.delete(db, id=company_id)

