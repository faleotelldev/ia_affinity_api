from sqlalchemy import Column, Integer, Float, Text, DateTime
from sqlalchemy.sql import func
from database import Base

class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, nullable=False)
    job_id = Column(Integer, nullable=False)
    affinity_score = Column(Float, nullable=False)
    match_reason = Column(Text, nullable=True)
    features_json = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ProcessorAgent:
    def process(self, candidate_skills, job_skills):
        cs = set(candidate_skills)
        js = set(job_skills)

        intersection = cs.intersection(js)
        union = cs.union(js)
        jaccard = (len(intersection) / len(union)) if union else 0.0

        return {
            "common_skills": len(intersection),
            "candidate_skills": list(cs),
            "job_skills": list(js),
            "jaccard": round(jaccard, 3)
        }
