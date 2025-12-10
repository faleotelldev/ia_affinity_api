from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.analysis import AnalysisCreate, AnalysisRead
from app.services import analysis_service

router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.post("/", response_model=AnalysisRead, status_code=status.HTTP_201_CREATED)
def run_analysis(payload: AnalysisCreate, db: Session = Depends(get_db)):
    """
    Ejecuta el pipeline completo (Extractor, Processor, AffinityScorer)
    y persiste el resultado en analysis_results.
    """
    result = analysis_service.run_affinity_pipeline(db, payload.candidate_id, payload.job_id)
    return result


@router.post("/run", response_model=AnalysisRead, status_code=status.HTTP_201_CREATED)
def run_analysis_alias(payload: AnalysisCreate, db: Session = Depends(get_db)):
    # Alias por si el profesor quiere /analysis/run
    return analysis_service.run_affinity_pipeline(db, payload.candidate_id, payload.job_id)


@router.get("/{analysis_id}", response_model=AnalysisRead)
def get_analysis(analysis_id: int, db: Session = Depends(get_db)):
    result = analysis_service.get_analysis_by_id(db, analysis_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis not found")
    return result


@router.get("/candidate/{candidate_id}", response_model=List[AnalysisRead])
def list_candidate_analysis(candidate_id: int, db: Session = Depends(get_db)):
    return analysis_service.get_analysis_by_candidate(db, candidate_id)


@router.get("/job/{job_id}", response_model=List[AnalysisRead])
def list_job_analysis(job_id: int, db: Session = Depends(get_db)):
    return analysis_service.get_analysis_by_job(db, job_id)
