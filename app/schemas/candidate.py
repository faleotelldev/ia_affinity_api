# app/schemas/candidate.py
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr


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
    created_at: Optional[datetime] = None   # <- CAMBIO IMPORTANTE
    updated_at: Optional[datetime] = None   # por coherencia

    model_config = ConfigDict(from_attributes=True)
