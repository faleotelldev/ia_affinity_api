from sqlalchemy.orm import Session
from app.services.candidate_service import list_candidates
from app.ai.algorithms import cluster_candidates

class AIService:
    @staticmethod
    def cluster_candidate_profiles(db: Session, n_clusters: int = 3):
        candidates = list_candidates(db)
        return cluster_candidates(candidates, n_clusters)
