from typing import List, Optional

from sqlalchemy.orm import Session

from app.models import Job, AnalysisResult
from app.schemas.job import JobCreate, JobUpdate


def get_job(db: Session, job_id: int) -> Optional[Job]:
    return db.query(Job).filter(Job.id == job_id).first()


def get_jobs(db: Session, skip: int = 0, limit: int = 100) -> List[Job]:
    return db.query(Job).offset(skip).limit(limit).all()


def create_job(db: Session, job_in: JobCreate) -> Job:
    job = Job(**job_in.dict())
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def update_job(db: Session, job_id: int, job_in: JobUpdate) -> Optional[Job]:
    job = get_job(db, job_id)
    if not job:
        return None

    data = job_in.dict(exclude_unset=True)
    for key, value in data.items():
        setattr(job, key, value)

    db.commit()
    db.refresh(job)
    return job


def delete_job(db: Session, job_id: int) -> bool:
    job = get_job(db, job_id)
    if not job:
        return False

    db.delete(job)
    db.commit()
    return True


def get_job_matches(db: Session, job_id: int) -> List[AnalysisResult]:
    return (
        db.query(AnalysisResult)
        .filter(AnalysisResult.job_id == job_id)
        .order_by(AnalysisResult.affinity_score.desc())
        .all()
    )
