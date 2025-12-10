# main.py
from fastapi import FastAPI

from app.database import Base, engine
from app.api import candidates, jobs, analysis

# Opcional: si tu BD ya está creada, esto no la rompe, solo verifica la estructura.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Affinity Matching API - IA")

# Healthcheck
@app.get("/health")
def health():
    return {"status": "ok"}


# Routers
app.include_router(candidates.router)
app.include_router(jobs.router)
app.include_router(analysis.router)
