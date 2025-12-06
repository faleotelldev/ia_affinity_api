from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.candidate import Candidate
from app.schemas.candidate import CandidateCreate, CandidateUpdate


def create_candidate(db: Session, data: CandidateCreate) -> Candidate:
    candidate = Candidate(**data.model_dump())
    db.add(candidate)
    db.commit()
    db.refresh(candidate)
    return candidate


def list_candidates(db: Session) -> List[Candidate]:
    return db.query(Candidate).all()


def get_candidate(db: Session, candidate_id: int) -> Optional[Candidate]:
    return db.query(Candidate).filter(Candidate.id == candidate_id).first()


def update_candidate(
    db: Session, candidate_id: int, data: CandidateUpdate
) -> Optional[Candidate]:
    candidate = get_candidate(db, candidate_id)
    if not candidate:
        return None

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(candidate, key, value)

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
