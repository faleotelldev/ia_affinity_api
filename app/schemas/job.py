from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class JobBase(BaseModel):
    title: str
    description: str
    location: Optional[str] = None
    salary_from: Optional[int] = None
    salary_to: Optional[int] = None


class JobCreate(JobBase):
    pass


class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    salary_from: Optional[int] = None
    salary_to: Optional[int] = None


class JobRead(JobBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
