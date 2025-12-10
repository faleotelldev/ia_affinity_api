# app/models/analysis_result.py
from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from app.database import Base


class AnalysisResult(Base):
    __tablename__ = "analysis_results"   # dbo.analysis_results

    id = Column("id", Integer, primary_key=True, index=True)
    candidate_id = Column("candidate_id", Integer, ForeignKey("candidates.id"), nullable=False)
    job_id = Column("job_id", Integer, ForeignKey("jobs.id"), nullable=False)
    affinity_score = Column("affinity_score", Float, nullable=False)
    match_reason = Column("match_reason", String(2000), nullable=False)
    features_json = Column("features_json", String(4000), nullable=False)
    created_at = Column("created_at", DateTime(timezone=True), nullable=True, default=datetime.utcnow)
