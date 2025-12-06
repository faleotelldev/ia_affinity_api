# app/api/analysis.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from app.services.analysis_service import AnalysisService
from app.repositories.analysis_repository import AnalysisRepository


router = APIRouter(prefix="/analysis", tags=["Analysis"])

# clásico (si lo quieres mantener)
@router.get("/classic/{candidate_id}/{job_id}")
def analyze_classic(candidate_id: int, job_id: int, db: Session = Depends(get_db)):
    res = AnalysisService().calculate_affinity(db, candidate_id, job_id)
    if not res:
        raise HTTPException(status_code=404, detail="Candidate or Job not found")
    return res

# POST: ejecutar pipeline IA y guardar (por ids)
@router.post("/")
def analyze_and_save(payload: dict, db: Session = Depends(get_db)):
    candidate_id = payload.get("candidate_id")
    job_id = payload.get("job_id")
    if not candidate_id or not job_id:
        raise HTTPException(status_code=400, detail="candidate_id and job_id are required")
    svc = AnalysisService(use_deepseek_score=False)  # cambiar True para scoring por DeepSeek
    saved = svc.analyze_and_save_by_ids(db, candidate_id, job_id)
    if not saved:
        raise HTTPException(status_code=404, detail="Candidate or Job not found")
    return {"status": "saved", "analysis_id": saved.id, "result": saved.result_json}

# GET: recuperar análisis por id
@router.get("/{analysis_id}")
def get_analysis(analysis_id: int, db: Session = Depends(get_db)):
    ar = AnalysisRepository.get_analysis(db, analysis_id)
    if not ar:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return ar.result_json

# compare endpoint
@router.get("/compare/{candidate_id}/{job_id}")
def compare(candidate_id: int, job_id: int, db: Session = Depends(get_db)):
    svc = AnalysisService(use_deepseek_score=True)  # use DeepSeek for pipeline scoring
    classic = AnalysisService.calculate_affinity(db, candidate_id, job_id)
    deep = svc.analyze_by_ids(db, candidate_id, job_id)
    if classic is None or deep is None:
        raise HTTPException(status_code=404, detail="Candidate or Job not found")
    return {"classic_affinity": classic, "ia_pipeline_affinity": deep}
