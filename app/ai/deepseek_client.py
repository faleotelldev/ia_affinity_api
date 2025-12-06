# app/ai/deepseek_client.py
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_URL = "https://api.deepseek.com/chat/completions"

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
}

def ask_deepseek(prompt: str) -> dict:
    """
    Llama a DeepSeek y devuelve un dict (parsed JSON) si el modelo responde JSON,
    o un dict con {"text": "..."} si devuelve texto libre.
    """
    body = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        # ajusta otros parámetros si DeepSeek lo soporta (temperature, max_tokens, etc.)
    }

    resp = requests.post(DEEPSEEK_URL, json=body, headers=HEADERS, timeout=30)
    if resp.status_code != 200:
        raise Exception(f"DeepSeek error ({resp.status_code}): {resp.text}")

    j = resp.json()
    # intentar extraer contenido esperado
    try:
        content = j["choices"][0]["message"]["content"]
    except Exception:
        # fallback, devolver todo
        return {"text": j}

    # intentar parsear JSON si el modelo devolvió JSON textual
    content_str = content.strip()
    try:
        parsed = json.loads(content_str)
        return parsed
    except Exception:
        # No JSON válido: devolver en campo text
        return {"text": content_str}
