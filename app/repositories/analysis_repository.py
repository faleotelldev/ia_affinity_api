# app/repositories/analysis_repository.py
import json
from sqlalchemy.orm import Session
from app.models.analysis_result import AnalysisResult

class AnalysisRepository:

    @staticmethod
    def save_analysis(db: Session, candidate_id: int, job_id: int, result: dict):
        # Convertir matching_skills a CSV seguro y result dict a string JSON
        matching = result.get("matching_skills", [])
        if isinstance(matching, list):
            matching_str = ",".join([str(s) for s in matching])
        else:
            matching_str = str(matching)

        # Serializar result completo (asegúrate de que todo sea serializable)
        try:
            result_serialized = json.dumps(result, default=str)
        except Exception:
            # fallback: convertir los valores no serializables a str
            safe = {k: (v if isinstance(v, (str, int, float, bool, list, dict, type(None))) else str(v)) for k, v in result.items()}
            result_serialized = json.dumps(safe, default=str)

        analysis = AnalysisResult(
            candidate_id=candidate_id,
            job_id=job_id,
            matching_skills=matching_str,
            score=float(result.get("score", 0)),
            result_json=result_serialized
        )
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        return analysis

    @staticmethod
    def get_analysis(db: Session, analysis_id: int):
        ar = db.query(AnalysisResult).filter(AnalysisResult.id == analysis_id).first()
        if not ar:
            return None
        # devolver el JSON parseado
        try:
            parsed = json.loads(ar.result_json)
        except Exception:
            parsed = {"raw": ar.result_json}
        return parsed
