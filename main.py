# main.py
from fastapi import FastAPI

from database import Base, engine
from app.api import candidates, jobs  # si tienes __init__.py que exporta routers
from app.api import analysis

app = FastAPI(title="Affinity Matching API - IA")


@app.on_event("startup")
def on_startup():
    # Solo para desarrollo: asegura que los modelos coinciden con las tablas.
    Base.metadata.create_all(bind=engine)


app.include_router(candidates.router)
app.include_router(jobs.router)
app.include_router(analysis.router)


@app.get("/")
def root():
    return {"status": "ok", "message": "API running with Azure SQL"}
