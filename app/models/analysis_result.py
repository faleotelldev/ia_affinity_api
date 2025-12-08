# app/models/analysis_result.py
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from database import Base
from datetime import datetime

class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    affinity_score = Column(Float, nullable=False)
    match_reason = Column(String, nullable=True)
    features_json = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
