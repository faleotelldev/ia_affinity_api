# app/services/analysis_service.py
from sqlalchemy.orm import Session

from app.models import AnalysisResult
from app.schemas.analysis import AnalysisRequest
from app.services.agents.extractor_agent import ExtractorAgent
from app.services.agents.processor_agent import ProcessorAgent
from app.services.agents.affinity_scorer_agent import AffinityScorerAgent


def run_affinity_pipeline(db: Session, request: AnalysisRequest) -> AnalysisResult:
    extractor = ExtractorAgent(db)
    processor = ProcessorAgent()
    scorer = AffinityScorerAgent()

    candidate, job = extractor.load_candidate_and_job(
        candidate_id=request.candidate_id,
        job_id=request.job_id,
    )

    if not candidate or not job:
        raise ValueError("Candidate or Job not found")

    features = processor.build_features(candidate, job)
    features_json = processor.to_json(features)
    affinity_score, match_reason = scorer.score(features)

    analysis = AnalysisResult(
        candidate_id=request.candidate_id,
        job_id=request.job_id,
        affinity_score=affinity_score,
        match_reason=match_reason,
        features_json=features_json,
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    return analysis


def get_analysis_by_id(db: Session, analysis_id: int):
    return db.query(AnalysisResult).filter(AnalysisResult.id == analysis_id).first()


def get_analysis_by_candidate(db: Session, candidate_id: int):
    return (
        db.query(AnalysisResult)
        .filter(AnalysisResult.candidate_id == candidate_id)
        .order_by(AnalysisResult.affinity_score.desc())
        .all()
    )


def get_analysis_by_job(db: Session, job_id: int):
    return (
        db.query(AnalysisResult)
        .filter(AnalysisResult.job_id == job_id)
        .order_by(AnalysisResult.affinity_score.desc())
        .all()
    )
