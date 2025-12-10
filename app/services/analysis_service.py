import json
from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import Candidate, Job, AnalysisResult
from .agents import ExtractorAgent, ProcessorAgent, AffinityScorerAgent


def run_affinity_pipeline(db: Session, candidate_id: int, job_id: int) -> AnalysisResult:
    candidate: Optional[Candidate] = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    job: Optional[Job] = db.query(Job).filter(Job.id == job_id).first()

    if not candidate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Candidate not found")
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    extractor = ExtractorAgent()
    processor = ProcessorAgent()
    scorer = AffinityScorerAgent()

    raw_features = extractor.extract(candidate, job)
    processed_features = processor.process(raw_features)
    score, reason = scorer.score(processed_features)

    result = AnalysisResult(
        candidate_id=candidate.id,
        job_id=job.id,
        affinity_score=score,
        match_reason=reason,
        features_json=json.dumps(processed_features),
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    return result


def get_analysis_by_id(db: Session, analysis_id: int) -> Optional[AnalysisResult]:
    return db.query(AnalysisResult).filter(AnalysisResult.id == analysis_id).first()


def get_analysis_by_candidate(db: Session, candidate_id: int) -> List[AnalysisResult]:
    return (
        db.query(AnalysisResult)
        .filter(AnalysisResult.candidate_id == candidate_id)
        .order_by(AnalysisResult.created_at.desc())
        .all()
    )


def get_analysis_by_job(db: Session, job_id: int) -> List[AnalysisResult]:
    return (
        db.query(AnalysisResult)
        .filter(AnalysisResult.job_id == job_id)
        .order_by(AnalysisResult.created_at.desc())
        .all()
    )
