from app.models import Candidate, Job


class ExtractorAgent:
    """
    Extrae features simples a partir de las habilidades del candidato y de la oferta.
    """

    def extract(self, candidate: Candidate, job: Job) -> dict:
        candidate_skills = {s.strip().lower() for s in candidate.skills.split(",")}
        job_skills = {s.strip().lower() for s in job.description.split(",")}

        overlap = candidate_skills.intersection(job_skills)
        features = {
            "skill_overlap_count": len(overlap),
            "candidate_skills_count": len(candidate_skills),
            "job_skills_count": len(job_skills),
            "years_experience": candidate.years_experience,
        }
        return features
