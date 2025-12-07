from typing import List
'''
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import SessionLocal
from app.schemas.candidate import CandidateCreate, CandidateRead, CandidateUpdate
from app.services.candidate_service import (
    create_candidate,
    list_candidates,
    get_candidate,
    update_candidate,
    delete_candidate,
)

router = APIRouter(prefix="/candidates", tags=["Candidates"])
'''
# app/api/candidates.py
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from database import SessionLocal
from app.schemas.candidate import CandidateRead, CandidateCreate, CandidateUpdate, CandidateMatch
from app.schemas.job import JobMatch
from app.services.affinity_service import get_best_jobs_for_candidate
from app.services.candidate_service import (
    create_candidate,
    list_candidates,
    get_candidate,
    update_candidate,
    delete_candidate,
)

router = APIRouter(prefix="/candidates", tags=["Candidates"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#@router.post(
#    "/", response_model=CandidateRead, status_code=status.HTTP_201_CREATED
#)
#def create_candidate_endpoint(
#    data: CandidateCreate, db: Session = Depends(get_db)
#):
#    return create_candidate(db, data)

@router.post("/", response_model=CandidateRead, status_code=status.HTTP_201_CREATED)
def create_candidate_endpoint(candidate: CandidateCreate, db: Session = Depends(get_db)):
    try:
        return create_candidate(db, candidate)
    except Exception as e:
        # ⚠️ Solo para depurar en desarrollo
        print("ERROR EN CREATE CANDIDATE:", repr(e))
        raise HTTPException(
            status_code=500,
            detail=f"Internal error: {e}"
        )

@router.get("/", response_model=List[CandidateRead])
def list_candidates_endpoint(db: Session = Depends(get_db)):
    return list_candidates(db)


@router.get("/{candidate_id}", response_model=CandidateRead)
def get_candidate_endpoint(candidate_id: int, db: Session = Depends(get_db)):
    candidate = get_candidate(db, candidate_id)
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found",
        )
    return candidate


@router.put("/{candidate_id}", response_model=CandidateRead)
def update_candidate_endpoint(
    candidate_id: int,
    data: CandidateUpdate,
    db: Session = Depends(get_db),
):
    candidate = update_candidate(db, candidate_id, data)
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
    # 204 no content → no body

@router.get("/{candidate_id}/matches", response_model=list[JobMatch])
def get_candidate_matches(
    candidate_id: int,
    min_score: float = Query(0, ge=0, le=100),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    matches = get_best_jobs_for_candidate(
        db=db,
        candidate_id=candidate_id,
        min_score=min_score,
        limit=limit,
    )

    result: list[JobMatch] = []
    for job, score in matches:
        result.append(JobMatch(job=job, score=score))
    return result   
