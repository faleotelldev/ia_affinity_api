# app/models/candidate.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base


class Candidate(Base):
    __tablename__ = "candidates"   # dbo.candidates

    id = Column("id", Integer, primary_key=True, index=True)
    name = Column("name", String(255), nullable=False)
    email = Column("email", String(255), nullable=False)
    skills = Column("skills", String(1000), nullable=True)
    years_experience = Column("years_experience", Integer, nullable=False)
    created_at = Column("created_at", DateTime(timezone=True), nullable=True, default=datetime.utcnow)
    updated_at = Column("updated_at", DateTime(timezone=True), nullable=True)
