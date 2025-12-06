# app/models/analysis_result.py
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from database import Base  # usa database (está en raíz)

class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)

    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)

    matching_skills = Column(String(1000), nullable=True)  # lista guardada como texto (csv)
    score = Column(Float, nullable=False)

    # Guardamos el JSON serializado como texto para compatibilidad con SQL Server
    result_json = Column(Text, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
