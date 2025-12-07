# app/services/affinity_service.py
import json
from typing import List, Tuple

from sqlalchemy.orm import Session

from app.models import Candidate, Job, AnalysisResult


def _normalize_list(text: str | None) -> List[str]:
    """Convert a comma-separated string into a normalized list of tokens."""
    if not text:
        return []
    return [p.strip().lower() for p in text.split(",") if p.strip()]


def compute_affinity(candidate: Candidate, job: Job) -> Tuple[float, str, dict]:
    """
    Compute a simple affinity score between a candidate and a job.

    - Compare candidate.skills vs job.description (both treated as comma-separated skills).
    - Add small bonus if years_experience > 0 (puedes ajustar luego).
    """
    cand_skills = _normalize_list(candidate.skills)
    job_skills = _normalize_list(job.description)  # we assume description contains skills

    if not job_skills:
        return 0.0, "No skills defined for job", {}

    matches = list(set(cand_skills) & set(job_skills))
    skills_score = len(matches) / len(job_skills)  # 0.0 – 1.0

    # Small bonus for experience
    exp_bonus = 0.0
    if candidate.years_experience and candidate.years_experience > 0:
        exp_bonus = 0.1  # +10%

    final_score = (skills_score + exp_bonus) * 100
    final_score = max(0.0, min(final_score, 100.0))

    reason = f"{len(matches)} skill(s) matched: {', '.join(matches)}"
    features = {
        "candidate_skills": cand_skills,
        "job_skills": job_skills,
        "matches": matches,
        "skills_score": skills_score,
        "experience_years": candidate.years_experience,
        "exp_bonus": exp_bonus,
    }

    return final_score, reason, features


def analyze_candidate_job(
    db: Session,
    candidate_id: int,
    job_id: int,
) -> AnalysisResult:
    """
    Run affinity analysis for one candidate-job pair and store it in analysis_results.
    """
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    job = db.query(Job).filter(Job.id == job_id).first()

    if not candidate or not job:
        raise ValueError("Candidate or Job not found")

    score, reason, features = compute_affinity(candidate, job)

    result = AnalysisResult(
        candidate_id=candidate.id,
        job_id=job.id,
        affinity_score=score,
        match_reason=reason,
        features_json=json.dumps(features),
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    return result


def get_best_jobs_for_candidate(
    db: Session,
    candidate_id: int,
    min_score: float = 0,
    limit: int = 10,
):
    """
    Compute affinity for all jobs with a given candidate (on the fly).
    Returns a list of (Job, score).
    """
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        return []

    jobs = db.query(Job).all()
    scored = []

    for job in jobs:
        score, _, _ = compute_affinity(candidate, job)
        if score >= min_score:
            scored.append((job, score))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:limit]


def get_best_candidates_for_job(
    db: Session,
    job_id: int,
    min_score: float = 0,
    limit: int = 10,
):
    """
    Compute affinity for all candidates with a given job (on the fly).
    Returns a list of (Candidate, score).
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        return []

    candidates = db.query(Candidate).all()
    scored = []

    for candidate in candidates:
        score, _, _ = compute_affinity(candidate, job)
        if score >= min_score:
            scored.append((candidate, score))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:limit]
