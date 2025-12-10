# app/services/agents/extractor_agent.py
from sqlalchemy.orm import Session
from app.models import Candidate, Job


class ExtractorAgent:
    def __init__(self, db: Session):
        self.db = db

    def load_candidate_and_job(self, candidate_id: int, job_id: int):
        candidate = self.db.query(Candidate).filter(Candidate.id == candidate_id).first()
        job = self.db.query(Job).filter(Job.id == job_id).first()
        return candidate, job
