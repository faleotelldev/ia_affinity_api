# app/services/agents/affinity_scorer_agent.py
from app.services.agents.processor_agent import ProcessedFeatures


class AffinityScorerAgent:
    def score(self, features: ProcessedFeatures) -> tuple[float, str]:
        if not features.job_keywords:
            return 0.0, "Oferta sin descripción detallada"

        matches = [
            skill for skill in features.candidate_skills
            if skill in features.job_keywords
        ]
        base_score = len(matches) / len(features.job_keywords)

        exp_bonus = min(features.years_experience / 10, 1.0)

        score = (0.7 * base_score) + (0.3 * exp_bonus)
        score = round(score * 100, 2)

        reason = f"{len(matches)} habilidades coinciden; experiencia: {features.years_experience} años"
        return score, reason
