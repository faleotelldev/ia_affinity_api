# app/api/analysis.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.analysis import (
    AnalysisRequest,
    AnalysisResultRead,
)
from app.services import analysis_service

router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.post("/", response_model=AnalysisResultRead, status_code=status.HTTP_201_CREATED)
def run_analysis(request: AnalysisRequest, db: Session = Depends(get_db)):
    try:
        analysis = analysis_service.run_affinity_pipeline(db, request)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return analysis


@router.post("/run", response_model=AnalysisResultRead, status_code=status.HTTP_201_CREATED)
def run_analysis_alias(request: AnalysisRequest, db: Session = Depends(get_db)):
    return run_analysis(request, db)


@router.get("/{analysis_id}", response_model=AnalysisResultRead)
def get_analysis(analysis_id: int, db: Session = Depends(get_db)):
    analysis = analysis_service.get_analysis_by_id(db, analysis_id)
    if not analysis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis not found")
    return analysis


@router.get("/candidate/{candidate_id}", response_model=List[AnalysisResultRead])
def list_candidate_analysis(candidate_id: int, db: Session = Depends(get_db)):
    return analysis_service.get_analysis_by_candidate(db, candidate_id)


@router.get("/job/{job_id}", response_model=List[AnalysisResultRead])
def list_job_analysis(job_id: int, db: Session = Depends(get_db)):
    return analysis_service.get_analysis_by_job(db, job_id)
