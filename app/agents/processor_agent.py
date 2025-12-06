# app/agents/processor_agent.py
class ProcessorAgent:
    @staticmethod
    def process_extracted(extracted: dict) -> dict:
        """
        Normaliza skills: lower, strip, unicos.
        Mantiene experience_years.
        """
        raw_skills = extracted.get("skills", []) or []
        normalized = []
        for s in raw_skills:
            if not isinstance(s, str):
                continue
            ss = s.strip().lower()
            if ss:
                normalized.append(ss)
        normalized = list(dict.fromkeys(normalized))  # mantiene orden y quita duplicados
        return {
            "skills": normalized,
            "experience_years": extracted.get("experience_years", 0)
        }

    @staticmethod
    def process_job_text(job_data: dict) -> dict:
        """
        En caso de que la oferta no venga con 'skills', intenta extraer tokens desde description.
        """
        desc = job_data.get("description") or ""
        # simple split por , ; | \n y limpieza
        tokens = [t.strip().lower() for t in desc.replace(";",",").replace("|",",").replace("\n",",").split(",") if t.strip()]
        unique = list(dict.fromkeys(tokens))
        return {"skills": unique}
