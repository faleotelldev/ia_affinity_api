# app/api/candidates.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.candidate import CandidateCreate, CandidateUpdate, CandidateRead
from app.services.candidate_service import (
    get_candidates,
    get_candidate_by_id,
    create_candidate,
    update_candidate,
    delete_candidate,
)

router = APIRouter(prefix="/candidates", tags=["candidates"])


@router.get("/", response_model=List[CandidateRead])
def list_candidates(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    # DEBUG opcional
    print(f"[DEBUG] list_candidates skip={skip} limit={limit}")
    candidates = get_candidates(db, skip=skip, limit=limit)
    return candidates


@router.get("/{candidate_id}", response_model=CandidateRead)
def get_candidate(candidate_id: int, db: Session = Depends(get_db)):
    candidate = get_candidate_by_id(db, candidate_id)
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found",
        )
    return candidate


@router.post("/", response_model=CandidateRead, status_code=status.HTTP_201_CREATED)
def create_candidate_endpoint(
    candidate_in: CandidateCreate,
    db: Session = Depends(get_db),
):
    return create_candidate(db, candidate_in)


@router.put("/{candidate_id}", response_model=CandidateRead)
def update_candidate_endpoint(
    candidate_id: int,
    candidate_in: CandidateUpdate,
    db: Session = Depends(get_db),
):
    candidate = update_candidate(db, candidate_id, candidate_in)
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found",
        )
    return candidate


@router.delete("/{candidate_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_candidate_endpoint(candidate_id: int, db: Session = Depends(get_db)):
    ok = delete_candidate(db, candidate_id)
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found",
        )
    return None
