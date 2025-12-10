# app/services/candidate_service.py
from sqlalchemy.orm import Session
from app.models import Candidate, AnalysisResult
from app.schemas.candidate import CandidateCreate, CandidateUpdate


def get_candidates(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(Candidate)
        .order_by(Candidate.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_candidate(db: Session, candidate_id: int):
    return db.query(Candidate).filter(Candidate.id == candidate_id).first()


def create_candidate(db: Session, candidate_in: CandidateCreate):
    candidate = Candidate(**candidate_in.model_dump())
    db.add(candidate)
    db.commit()
    db.refresh(candidate)
    return candidate


def update_candidate(db: Session, candidate_id: int, candidate_in: CandidateUpdate):
    candidate = get_candidate(db, candidate_id)
    if not candidate:
        return None
    for field, value in candidate_in.model_dump(exclude_unset=True).items():
        setattr(candidate, field, value)
    db.commit()
    db.refresh(candidate)
    return candidate


def delete_candidate(db: Session, candidate_id: int) -> bool:
    candidate = get_candidate(db, candidate_id)
    if not candidate:
        return False
    db.delete(candidate)
    db.commit()
    return True


def get_candidate_matches(db: Session, candidate_id: int):
    return (
        db.query(AnalysisResult)
        .filter(AnalysisResult.candidate_id == candidate_id)
        .order_by(AnalysisResult.affinity_score.desc())
        .all()
    )
