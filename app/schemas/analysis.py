from datetime import datetime

from pydantic import BaseModel


class AnalysisCreate(BaseModel):
    candidate_id: int
    job_id: int


class AnalysisRead(BaseModel):
    id: int
    candidate_id: int
    job_id: int
    affinity_score: float
    match_reason: str
    features_json: str
    created_at: datetime

    class Config:
        from_attributes = True
