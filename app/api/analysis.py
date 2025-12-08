# app/api/analysis.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from app.services.analysis_service import AnalysisService
from app.repositories.analysis_repository import AnalysisRepository

router = APIRouter(prefix="/analysis", tags=["Analysis"])


# ⭐ Clásico (no IA)
@router.get("/classic/{candidate_id}/{job_id}")
def analyze_classic(candidate_id: int, job_id: int, db: Session = Depends(get_db)):
    res = AnalysisService().calculate_affinity(db, candidate_id, job_id)
    if not res:
        raise HTTPException(status_code=404, detail="Candidate or Job not found")
    return res


# 🚀 Ejecutar pipeline IA y guardar resultado en DB
@router.post("/")
def analyze_and_save(payload: dict, db: Session = Depends(get_db)):
    candidate_id = payload.get("candidate_id")
    job_id = payload.get("job_id")

    if not candidate_id or not job_id:
        raise HTTPException(status_code=400, detail="candidate_id and job_id are required")

    svc = AnalysisService(use_deepseek_score=True)  # IA
    saved = svc.analyze_and_save_by_ids(db, candidate_id, job_id)

    if not saved:
        raise HTTPException(status_code=404, detail="Candidate or Job not found")

    return {
    "status": "saved",
    "analysis_id": saved.id,
    "affinity_score": saved.affinity_score,
    "match_reason": saved.match_reason,
    "features": saved.features_json
    }




# 📌 Obtener resultado guardado desde DB
@router.get("/{analysis_id}")
def get_analysis(analysis_id: int, db: Session = Depends(get_db)):
    record = AnalysisRepository.get_analysis(db, analysis_id)
    if not record:
        raise HTTPException(status_code=404, detail="Analysis not found")

    return {
        "id": record.id,
        "candidate_id": record.candidate_id,
        "job_id": record.job_id,
        "affinity_score": record.affinity_score,
        "match_reason": record.match_reason,
        "features": record.features_json,
        "created_at": record.created_at,
    }


# 🔄 Comparación clásico vs IA (solo ejecuta IA, no guarda)
@router.get("/compare/{candidate_id}/{job_id}")
def compare(candidate_id: int, job_id: int, db: Session = Depends(get_db)):
    svc = AnalysisService(use_deepseek_score=True)  # IA
    classic = AnalysisService.calculate_affinity(db, candidate_id, job_id)
    deep = svc.analyze_by_ids(db, candidate_id, job_id)

    if classic is None or deep is None:
        raise HTTPException(status_code=404, detail="Candidate or Job not found")

    return {
        "classic_affinity": classic,
        "ia_pipeline_affinity": deep
    }
