# app/agents/orchestrator.py
from .extractor_agent import ExtractorAgent
from .processor_agent import ProcessorAgent
from .affinity_scorer_agent import AffinityScorerAgent

class CrewOrchestrator:
    def __init__(self, use_deepseek_for_scoring: bool = False):
        self.extractor = ExtractorAgent()
        self.processor = ProcessorAgent()
        self.scorer = AffinityScorerAgent()
        self.use_deepseek_for_scoring = use_deepseek_for_scoring

    def run(self, candidate_data: dict, job_data: dict) -> dict:
        # 1) Extract (DeepSeek)
        extracted_cand = self.extractor.extract(candidate_data, job_data)
        # 2) Process candidate
        cand_proc = self.processor.process_extracted(extracted_cand)
        # 3) Process job (either use extracted skills if provided, or parse description)
        job_proc = self.processor.process_job_text(job_data) if not job_data.get("skills") else {"skills": [s.strip().lower() for s in job_data.get("skills", "").split(",")]}
        # 4) Score
        score = self.scorer.score(cand_proc, job_proc)


        # final output
        return {
            "candidate": candidate_data.get("name"),
            "candidate_id": candidate_data.get("id"),
            "job": job_data.get("title"),
            "job_id": job_data.get("id"),
            "matching_skills": score["matching_skills"],
            "score": score["score"],
            "method": score.get("method", "deepseek"),
            "candidate_skills_processed": cand_proc.get("skills", []),
            "job_skills_processed": job_proc.get("skills", [])
        }
