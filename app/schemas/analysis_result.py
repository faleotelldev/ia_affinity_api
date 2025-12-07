# app/schemas/analysis_result.py
from datetime import datetime
from typing import Optional, Any

from pydantic import BaseModel


class AnalysisResultBase(BaseModel):
    candidate_id: int
    job_id: int
    affinity_score: float
    match_reason: Optional[str] = None
    features_json: Optional[str] = None  # guardamos JSON como string


class AnalysisResultCreate(AnalysisResultBase):
    pass


class AnalysisResultRead(AnalysisResultBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
