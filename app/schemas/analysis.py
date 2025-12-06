from pydantic import BaseModel

class AnalysisRequest(BaseModel):
    candidate_id: int
    job_id: int

class AnalysisResponse(BaseModel):
    analysis_id: int
    candidate_id: int
    job_id: int
    affinity_score: float
    match_reason: str
    features: dict
    created_at: str
