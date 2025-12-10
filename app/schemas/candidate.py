# app/schemas/candidate.py
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict


class CandidateBase(BaseModel):
    name: str
    email: EmailStr
    skills: str | None = None
    years_experience: int


class CandidateCreate(CandidateBase):
    pass


class CandidateUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    skills: str | None = None
    years_experience: int | None = None


class CandidateRead(CandidateBase):
    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
