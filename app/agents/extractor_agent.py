# app/agents/extractor_agent.py
from app.ai.deepseek_client import ask_deepseek
import json

class ExtractorAgent:
    """
    Llama a DeepSeek para extraer skills y años de experiencia.
    Espera que DeepSeek devuelva JSON como:
    {"skills": ["python", "sql"], "experience_years": 3}
    """

    @staticmethod
    def extract(candidate_data: dict, job_data: dict) -> dict:
        prompt = f"""
Analiza los siguientes datos y EXTRAER en formato JSON:
- skills: lista de habilidades (strings)
- experience_years: número de años relevantes si aparece (int)
Devuelve solo JSON.

CANDIDATO:
{candidate_data}

OFERTA:
{job_data}
"""
        result = ask_deepseek(prompt)

        # Si DeepSeek devolvió { "text": "..."} intentar extraer JSON dentro del texto
        if isinstance(result, dict) and "text" in result:
            text = result["text"]
            # intentar encontrar JSON en el texto
            try:
                start = text.index("{")
                end = text.rindex("}") + 1
                candidate_json = json.loads(text[start:end])
                return candidate_json
            except Exception:
                # fallback: devolver campos mínimos
                return {"skills": [], "experience_years": 0}
        # si ya es dict con skills/experience_years, devolverlo
        if isinstance(result, dict):
            return {
                "skills": result.get("skills", []),
                "experience_years": result.get("experience_years", result.get("experience", 0))
            }
        # fallback
        return {"skills": [], "experience_years": 0}
