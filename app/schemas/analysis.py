# app/schemas/analysis.py
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class AnalysisRequest(BaseModel):
    candidate_id: int
    job_id: int


class AnalysisResultBase(BaseModel):
    candidate_id: int
    job_id: int
    affinity_score: float
    match_reason: str
    features_json: str


class AnalysisResultCreate(AnalysisResultBase):
    pass


class AnalysisResultRead(AnalysisResultBase):
    id: int
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
