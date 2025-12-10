# app/api/candidates.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.candidate import CandidateCreate, CandidateUpdate, CandidateRead
from app.schemas.analysis import AnalysisResultRead
from app.services import candidate_service

router = APIRouter(prefix="/candidates", tags=["candidates"])


@router.get("/", response_model=List[CandidateRead])
def list_candidates(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return candidate_service.get_candidates(db, skip=skip, limit=limit)


@router.post("/", response_model=CandidateRead, status_code=status.HTTP_201_CREATED)
def create_candidate(candidate_in: CandidateCreate, db: Session = Depends(get_db)):
    return candidate_service.create_candidate(db, candidate_in)


@router.get("/{candidate_id}", response_model=CandidateRead)
def get_candidate(candidate_id: int, db: Session = Depends(get_db)):
    candidate = candidate_service.get_candidate(db, candidate_id)
    if not candidate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Candidate not found")
    return candidate


@router.put("/{candidate_id}", response_model=CandidateRead)
def update_candidate(candidate_id: int, candidate_in: CandidateUpdate, db: Session = Depends(get_db)):
    candidate = candidate_service.update_candidate(db, candidate_id, candidate_in)
    if not candidate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Candidate not found")
    return candidate


@router.delete("/{candidate_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_candidate(candidate_id: int, db: Session = Depends(get_db)):
    ok = candidate_service.delete_candidate(db, candidate_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Candidate not found")
    return None


@router.get("/{candidate_id}/matches", response_model=List[AnalysisResultRead])
def get_candidate_matches(candidate_id: int, db: Session = Depends(get_db)):
    return candidate_service.get_candidate_matches(db, candidate_id)
