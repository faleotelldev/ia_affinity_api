# app/services/candidate_service.py
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.candidate import Candidate
from app.schemas.candidate import CandidateCreate, CandidateUpdate

'''
def get_candidates(db: Session, skip: int = 0, limit: int = 100) -> List[Candidate]:
    return (
        db.query(Candidate)
        .offset(skip)
        .limit(limit)
        .all()
    )
'''
def get_candidates(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(Candidate)
        .order_by(Candidate.id)      # 👈 CLAVE PARA MSSQL
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_candidate_by_id(db: Session, candidate_id: int) -> Optional[Candidate]:
    return db.query(Candidate).filter(Candidate.id == candidate_id).first()


def create_candidate(db: Session, candidate_in: CandidateCreate) -> Candidate:
    db_candidate = Candidate(
        name=candidate_in.name,
        email=candidate_in.email,
        skills=candidate_in.skills,
        years_experience=candidate_in.years_experience,
    )
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)
    return db_candidate


def update_candidate(
    db: Session, candidate_id: int, candidate_in: CandidateUpdate
) -> Optional[Candidate]:
    db_candidate = get_candidate_by_id(db, candidate_id)
    if not db_candidate:
        return None

    data = candidate_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(db_candidate, field, value)

    db.commit()
    db.refresh(db_candidate)
    return db_candidate


def delete_candidate(db: Session, candidate_id: int) -> bool:
    db_candidate = get_candidate_by_id(db, candidate_id)
    if not db_candidate:
        return False

    db.delete(db_candidate)
    db.commit()
    return True
