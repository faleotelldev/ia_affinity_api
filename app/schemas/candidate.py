# app/schemas/candidate.py
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class CandidateBase(BaseModel):
    name: str
    email: EmailStr
    skills: Optional[str] = None
    years_experience: int


class CandidateCreate(CandidateBase):
    pass


class CandidateUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    skills: Optional[str] = None
    years_experience: Optional[int] = None


class CandidateRead(CandidateBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CandidateMatch(BaseModel):
    candidate: CandidateRead
    score: float

    class Config:
        from_attributes = True
