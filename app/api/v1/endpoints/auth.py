"""Authentication endpoints."""

from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api.deps import get_db
from app.core.security import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.crud import user as crud_user
from app.crud.crud_user_company_lookup import user_company_lookup as crud_lookup
from app.db.database import get_tenant_session
from app.models.company import Company
from app.schemas import Token, UserCreate, UserResponse

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_in: UserCreate,
    public_db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Register a new user.
    
    Args:
        user_in: User creation data (must include company_id)
        public_db: Public database session
        
    Returns:
        Created user
        
    Raises:
        HTTPException: If email already registered or company doesn't exist
    """
    # Validate company_id is provided
    if not user_in.company_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="company_id is required for registration",
        )
    
    # Validate company exists
    result = await public_db.execute(
        select(Company).filter(Company.id == user_in.company_id)
    )
    company = result.scalar_one_or_none()
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found",
        )
    
    # Check if email already registered in lookup table
    existing_lookup = await crud_lookup.get_by_email(public_db, email=user_in.email)
    if existing_lookup:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    # Create user in tenant schema
    async for tenant_db in get_tenant_session(user_in.company_id):
        # Check if user exists in tenant schema (extra safety)
        existing_user = await crud_user.get_by_email(tenant_db, email=user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        
        # Create user in tenant schema
        user = await crud_user.create(tenant_db, obj_in=user_in)
        
        # Create lookup entry in public schema
        await crud_lookup.create_entry(
            public_db, email=user.email, company_id=user_in.company_id
        )
        
        return user


@router.post("/login", response_model=Token)
async def login(
    public_db: AsyncSession = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """
    OAuth2 compatible token login.
    
    Args:
        public_db: Public database session
        form_data: OAuth2 form data (username and password)
        
    Returns:
        Access token with company_id
        
    Raises:
        HTTPException: If credentials are invalid
    """
    # Step 1: Look up company_id from email
    lookup = await crud_lookup.get_by_email(public_db, email=form_data.username)
    if not lookup:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    company_id = lookup.company_id
    
    # Step 2: Authenticate user from tenant schema
    async for tenant_db in get_tenant_session(company_id):
        user = await crud_user.authenticate(
            tenant_db, email=form_data.username, password=form_data.password
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )
        
        # Step 3: Create access token with company_id
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email, "company_id": company_id},
            expires_delta=access_token_expires
        )
        
        return {"access_token": access_token, "token_type": "bearer"}

