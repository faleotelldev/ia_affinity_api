# app/schemas/job.py
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class JobBase(BaseModel):
    title: str
    description: str | None = None
    location: str | None = None
    skills: str | None = None    # 👈 lo usamos solo a nivel de API
    salary_from: int | None = None
    salary_to: int | None = None


class JobCreate(JobBase):
    pass


class JobUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    location: str | None = None
    skills: str | None = None
    salary_from: int | None = None
    salary_to: int | None = None


class JobRead(JobBase):
    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
