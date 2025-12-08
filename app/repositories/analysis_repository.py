# app/repositories/analysis_repository.py
import json
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.analysis_result import AnalysisResult

class AnalysisRepository:

    @staticmethod
    def save_analysis(db: Session, candidate_id, job_id, affinity_score, match_reason, features_json):
        new_analysis = AnalysisResult(
            candidate_id=candidate_id,
            job_id=job_id,
            affinity_score=affinity_score,
            match_reason=match_reason,
            features_json=json.dumps(features_json),
            created_at=datetime.utcnow()
        )

        db.add(new_analysis)
        db.commit()
        db.refresh(new_analysis)   # 👈 ESTO es importante

        return new_analysis         # 👈 Devuelve el modelo


    @staticmethod
    def get_analysis(db: Session, analysis_id: int):
        return db.query(AnalysisResult).filter(AnalysisResult.id == analysis_id).first()
