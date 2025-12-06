from fastapi import APIRouter
from app.ai.deepseek_client import ask_deepseek

router = APIRouter(prefix="/test", tags=["AI Test"])

@router.get("/deepseek")
def test_deepseek(prompt: str):
    """
    Envía un prompt a DeepSeek y retorna la respuesta.
    Ejemplo de uso:
    GET /test/deepseek?prompt=Hola
    """
    try:
        response = ask_deepseek(prompt)
        return {"prompt": prompt, "response": response}
    except Exception as e:
        return {"error": str(e)}
