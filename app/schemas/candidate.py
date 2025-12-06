from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class CandidateBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    email: EmailStr
    skills: Optional[str] = Field(
        default=None,
        description="Skills separados por coma, ej: Python,SQL,Azure"
    )
    years_experience: Optional[int] = Field(default=None, ge=0)


class CandidateCreate(CandidateBase):
    """Campos requeridos para crear candidato."""
    pass


class CandidateUpdate(BaseModel):
    """Campos opcionales para actualizar."""
    name: Optional[str] = Field(default=None, min_length=2, max_length=150)
    email: Optional[EmailStr] = None
    skills: Optional[str] = None
    years_experience: Optional[int] = Field(default=None, ge=0)


class CandidateRead(CandidateBase):
    """Respuesta hacia el cliente."""
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True   # antes orm_mode = True
