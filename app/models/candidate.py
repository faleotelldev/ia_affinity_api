# app/models/candidate.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from database import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    skills = Column(String, nullable=True)
    years_experience = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(DateTime(timezone=True), nullable=True)

    # Relationship to analysis_results
    analysis_results = relationship(
        "AnalysisResult",
        back_populates="candidate",
        cascade="all, delete-orphan",
    )
