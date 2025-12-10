# app/services/agents/orchestrator.py
import json
from sqlalchemy.orm import Session

from app.services.agents.extractor_agent import ExtractorAgent
from app.services.agents.processor_agent import ProcessorAgent
from app.services.agents.affinity_scorer_agent import AffinityScorerAgent
from app.models.analysis_result import AnalysisResult


class AffinityAnalysisOrchestrator:
    def __init__(self, db: Session):
        self.db = db
        self.extractor = ExtractorAgent(db)
        self.processor = ProcessorAgent()
        self.scorer = AffinityScorerAgent()

    def run(self, candidate_id: int, job_id: int) -> AnalysisResult:
        candidate, job = self.extractor.load_candidate_and_job(candidate_id, job_id)
        features = self.processor.build_features(candidate, job)
        affinity_score, match_reason = self.scorer.score(features)

        features_json = json.dumps(features, ensure_ascii=False)

        analysis = AnalysisResult(
            candidate_id=candidate.id,
            job_id=job.id,
            affinity_score=affinity_score,
            match_reason=match_reason,
            features_json=features_json,
        )
        self.db.add(analysis)
        self.db.commit()
        self.db.refresh(analysis)

        return analysis
