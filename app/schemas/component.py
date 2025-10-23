from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class ComponentCreate(BaseModel):
    name: str
    description: Optional[str] = None
    repository_url: Optional[str] = None
    is_managed: bool = True
    is_third_party: Optional[bool] = None
    company_id: int
    team_ids: List[int] = []
    tag_ids: List[int] = []
    container_image_ids: List[int] = []
    version_ids: List[int] = []


class ComponentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    repository_url: Optional[str] = None
    is_managed: Optional[bool] = None
    is_third_party: Optional[bool] = None
    company_id: Optional[int] = None
    team_ids: Optional[List[int]] = None
    tag_ids: Optional[List[int]] = None
    container_image_ids: Optional[List[int]] = None
    version_ids: Optional[List[int]] = None


class ComponentResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    repository_url: Optional[str]
    is_managed: bool
    is_third_party: Optional[bool]
    company_id: int
    team_ids: List[int]
    tag_ids: List[int]
    container_image_ids: List[int]
    version_ids: List[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

