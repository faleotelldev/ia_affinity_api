from typing import List

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
