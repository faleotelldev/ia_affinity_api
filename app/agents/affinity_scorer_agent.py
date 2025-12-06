class AffinityScorerAgent:

    def score(self, candidate_proc: dict, job_proc: dict) -> dict:
        cand_skills = set(candidate_proc.get("skills", []))
        job_skills = set(job_proc.get("skills", []))

        matches = list(cand_skills & job_skills)
        score = (len(matches) / len(job_skills)) * 100 if job_skills else 0

        return {
            "matching_skills": matches,
            "score": round(score, 2),
            "method": "deepseek"
        }
