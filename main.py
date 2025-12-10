# main.py
from fastapi import FastAPI

from app.database import Base, engine
from app.api import candidates, jobs, analysis  # importa routers

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Affinity Matching API - IA")

app.include_router(candidates.router)
app.include_router(jobs.router)
app.include_router(analysis.router)


@app.get("/")
def root():
    return {"status": "ok"}
