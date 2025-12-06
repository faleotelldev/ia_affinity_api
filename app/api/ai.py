from fastapi import APIRouter, Depends
from database import get_db
from app.services.ai_service import AIService

router = APIRouter(prefix="/ai", tags=["AI"])

@router.get("/clusters")
def get_candidate_clusters(db=Depends(get_db)):
    return AIService.cluster_candidate_profiles(db)
