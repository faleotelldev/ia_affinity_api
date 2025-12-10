class ProcessorAgent:
    """
    Procesa/normaliza features. Aquí lo dejamos muy simple.
    """

    def process(self, features: dict) -> dict:
        # Normalización muy básica
        processed = dict(features)
        max_skills = max(processed.get("candidate_skills_count", 1), 1)
        processed["skill_overlap_ratio"] = processed.get("skill_overlap_count", 0) / max_skills
        return processed
