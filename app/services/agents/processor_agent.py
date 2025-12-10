# app/services/agents/processor_agent.py
import json
from dataclasses import dataclass


@dataclass
class ProcessedFeatures:
    candidate_skills: list[str]
    job_keywords: list[str]
    years_experience: int


class ProcessorAgent:
    def build_features(self, candidate, job) -> ProcessedFeatures:
        candidate_skills = []
        if candidate.skills:
            candidate_skills = [s.strip().lower() for s in candidate.skills.split(",") if s.strip()]

        job_keywords = []
        if job.description:
            job_keywords = [w.strip().lower() for w in job.description.split() if len(w) > 3]

        return ProcessedFeatures(
            candidate_skills=candidate_skills,
            job_keywords=job_keywords,
            years_experience=candidate.years_experience,
        )

    def to_json(self, features: ProcessedFeatures) -> str:
        return json.dumps(features.__dict__, ensure_ascii=False)
