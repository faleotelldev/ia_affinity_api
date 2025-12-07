# app/api/analysis.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from app.schemas.analysis_result import AnalysisResultRead
from app.models import AnalysisResult
from app.services.affinity_service import analyze_candidate_job

router = APIRouter(prefix="/analysis", tags=["Analysis"])


@router.post("/run", response_model=AnalysisResultRead)
def run_analysis(
    candidate_id: int,
    job_id: int,
    db: Session = Depends(SessionLocal),
):
    try:
        result = analyze_candidate_job(db, candidate_id=candidate_id, job_id=job_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/candidate/{candidate_id}", response_model=list[AnalysisResultRead])
def list_candidate_analysis(
    candidate_id: int,
    db: Session = Depends(SessionLocal),
):
    results = (
        db.query(AnalysisResult)
        .filter(AnalysisResult.candidate_id == candidate_id)
        .order_by(AnalysisResult.created_at.desc())
        .all()
    )
    return results


@router.get("/job/{job_id}", response_model=list[AnalysisResultRead])
def list_job_analysis(
    job_id: int,
    db: Session = Depends(SessionLocal),
):
    results = (
        db.query(AnalysisResult)
        .filter(AnalysisResult.job_id == job_id)
        .order_by(AnalysisResult.created_at.desc())
        .all()
    )
    return results
