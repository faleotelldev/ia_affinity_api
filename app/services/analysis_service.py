# app/services/analysis_service.py
from sqlalchemy.orm import Session
import app.services.candidate_service as CandidateService
import app.services.job_service as JobService
from app.agents.orchestrator import CrewOrchestrator
from app.repositories.analysis_repository import AnalysisRepository

class AnalysisService:
    def __init__(self, use_deepseek_score: bool = False):
        self.orchestrator = CrewOrchestrator(use_deepseek_for_scoring=use_deepseek_score)

    def analyze_by_ids(self, db: Session, candidate_id: int, job_id: int):
        candidate = CandidateService.get_candidate(db, candidate_id)
        job = JobService.get_job(db, job_id)
        if not candidate or not job:
            return None
        candidate_data = {
            "id": candidate.id,
            "name": candidate.name,
            "skills": candidate.skills,
            "years_experience": candidate.years_experience
        }
        job_data = {
            "id": job.id,
            "title": job.title,
            "description": job.description
        }
        return self.orchestrator.run(candidate_data, job_data)

    def analyze_and_save_by_ids(self, db: Session, candidate_id: int, job_id: int):
        result = self.analyze_by_ids(db, candidate_id, job_id)
        if not result:
            return None
        saved = AnalysisRepository.save_analysis(db, candidate_id, job_id, result)
        return saved


    @staticmethod
    def calculate_affinity(db: Session, candidate_id: int, job_id: int) -> dict:
        candidate = CandidateService.get_candidate(db, candidate_id)
        job = JobService.get_job(db, job_id)

        if not candidate or not job:
            return None

        # Procesar skills del candidato
        candidate_skills = []
        if candidate.skills:
            candidate_skills = [
                s.strip().lower()
                for s in candidate.skills.replace(";", ",").replace("|", ",").split(",")
            ]

        # Procesar skills del trabajo
        job_skills = []
        if job.description:
            job_skills = [
                s.strip().lower()
                for s in job.description.replace(";", ",").replace("|", ",").split(",")
            ]

        # Calcular afinidad
        match = set(candidate_skills) & set(job_skills)
        score = (len(match) / len(job_skills)) * 100 if job_skills else 0

        return {
            "candidate": candidate.name,
            "job": job.title,
            "matching_skills": list(match),
            "score": round(score, 2)
        }
    
    
