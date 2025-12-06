from fastapi import FastAPI

from database import Base, engine
from app.api import analysis, candidates, jobs, ai, test_ai

app = FastAPI(title="Affinity Matching API - IA")

# Crear tablas al inicio (solo para dev)
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


# Incluir routers
app.include_router(candidates.router)
app.include_router(jobs.router)
app.include_router(analysis.router)
app.include_router(ai.router)
app.include_router(test_ai.router)


@app.get("/")
def root():
    return {"status": "ok", "message": "API running with Azure SQL"}
