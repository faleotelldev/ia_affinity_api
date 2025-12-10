# app/services/job_service.py
from sqlalchemy.orm import Session
from app.models import Job, AnalysisResult
from app.schemas.job import JobCreate, JobUpdate


def get_jobs(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(Job)
        .order_by(Job.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_job(db: Session, job_id: int):
    return db.query(Job).filter(Job.id == job_id).first()


def create_job(db: Session, job_in: JobCreate):
    job_data = job_in.model_dump()
    job_data.pop("skills", None)   # si no existe la columna en BD
    job = Job(**job_data)
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def update_job(db: Session, job_id: int, job_in: JobUpdate):
    job = get_job(db, job_id)
    if not job:
        return None
    data = job_in.model_dump(exclude_unset=True)
    data.pop("skills", None)
    for field, value in data.items():
        setattr(job, field, value)
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


def get_job_matches(db: Session, job_id: int):
    return (
        db.query(AnalysisResult)
        .filter(AnalysisResult.job_id == job_id)
        .order_by(AnalysisResult.affinity_score.desc())
        .all()
    )
