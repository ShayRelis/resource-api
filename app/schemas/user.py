from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from app.models import UserRole


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: Optional[str] = None
    company_id: Optional[int] = None
    role: UserRole = UserRole.user


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    company_id: Optional[int] = None
    is_active: Optional[bool] = None
    role: Optional[UserRole] = None


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str] = None
    company_id: Optional[int] = None
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str

