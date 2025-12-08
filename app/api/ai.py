from fastapi import APIRouter, Depends
from database import get_db
from app.services.ai_service import AIService
from app.services.candidate_service import list_candidates

router = APIRouter(prefix="/ai", tags=["AI"])

@router.get("/clusters/{n_clusters}")
def get_candidate_clusters(n_clusters: int, db=Depends(get_db)):
    data = AIService.cluster_candidate_profiles(db, n_clusters)
    candidates = list_candidates(db)

    labeled = {}
    for idx, cluster_id in enumerate(data["clusters"]):
        labeled.setdefault(cluster_id, []).append(candidates[idx].name)

    return {
        "total_candidates": len(candidates),
        "total_clusters": len(set(data["clusters"])),
        "selected_clusters": n_clusters,
        "clusters": labeled,
        "skills_features": data["skills"],
        "centroids": data["centroids"]
    }
