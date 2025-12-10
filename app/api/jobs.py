# app/api/jobs.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.job import JobCreate, JobUpdate, JobRead
from app.schemas.analysis import AnalysisResultRead
from app.services import job_service

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("/", response_model=List[JobRead])
def list_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return job_service.get_jobs(db, skip=skip, limit=limit)


@router.post("/", response_model=JobRead, status_code=status.HTTP_201_CREATED)
def create_job(job_in: JobCreate, db: Session = Depends(get_db)):
    return job_service.create_job(db, job_in)


@router.get("/{job_id}", response_model=JobRead)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = job_service.get_job(db, job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return job


@router.put("/{job_id}", response_model=JobRead)
def update_job(job_id: int, job_in: JobUpdate, db: Session = Depends(get_db)):
    job = job_service.update_job(db, job_id, job_in)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return job


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(job_id: int, db: Session = Depends(get_db)):
    ok = job_service.delete_job(db, job_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return None


@router.get("/{job_id}/matches", response_model=List[AnalysisResultRead])
def get_job_matches(job_id: int, db: Session = Depends(get_db)):
    return job_service.get_job_matches(db, job_id)
