from typing import List

'''
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import SessionLocal
from app.schemas.job import JobCreate, JobRead, JobUpdate
from app.services.job_service import (
    create_job,
    list_jobs,
    get_job,
    update_job,
    delete_job,
)

router = APIRouter(prefix="/jobs", tags=["Jobs"])
'''
# app/api/jobs.py
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session

from database import SessionLocal
from app.schemas.job import JobRead, JobCreate, JobUpdate
from app.schemas.candidate import CandidateMatch
from app.services.affinity_service import get_best_candidates_for_job
from app.services.job_service import (
    create_job,
    list_jobs,
    get_job,
    update_job,
    delete_job,
)

router = APIRouter(prefix="/jobs", tags=["Jobs"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=JobRead, status_code=status.HTTP_201_CREATED)
def create_job_endpoint(data: JobCreate, db: Session = Depends(get_db)):
    return create_job(db, data)


@router.get("/", response_model=List[JobRead])
def list_jobs_endpoint(db: Session = Depends(get_db)):
    return list_jobs(db)


@router.get("/{job_id}", response_model=JobRead)
def get_job_endpoint(job_id: int, db: Session = Depends(get_db)):
    job = get_job(db, job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )
    return job


@router.put("/{job_id}", response_model=JobRead)
def update_job_endpoint(
    job_id: int,
    data: JobUpdate,
    db: Session = Depends(get_db),
):
    job = update_job(db, job_id, data)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )
    return job


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job_endpoint(job_id: int, db: Session = Depends(get_db)):
    ok = delete_job(db, job_id)
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )
    
@router.get("/{job_id}/matches", response_model=list[CandidateMatch])
def get_job_matches(
    job_id: int,
    min_score: float = Query(0, ge=0, le=100),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    matches = get_best_candidates_for_job(
        db=db,
        job_id=job_id,
        min_score=min_score,
        limit=limit,
    )

    result: list[CandidateMatch] = []
    for candidate, score in matches:
        result.append(CandidateMatch(candidate=candidate, score=score))
    return result