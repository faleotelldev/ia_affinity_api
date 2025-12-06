# app/ai/algorithms.py

from sklearn.cluster import KMeans
import numpy as np

def vectorize_skills(candidates):
    """
    Recibe una lista de candidatos (objetos SQLAlchemy) y devuelve:
    1. vectores binarios
    2. lista de habilidades únicas globales
    """
    # Extraer y normalizar habilidades
    all_skills = set()
    candidate_skill_sets = []

    for c in candidates:
        if c.skills:
            skills = [s.strip().lower() for s in c.skills.replace(";",",").replace("|",",").split(",")]
        else:
            skills = []
        candidate_skill_sets.append(skills)
        all_skills.update(skills)

    all_skills = sorted(list(all_skills))  # Lista final de features

    # Crear matriz binaria
    vectors = []
    for skills in candidate_skill_sets:
        vector = [1 if skill in skills else 0 for skill in all_skills]
        vectors.append(vector)

    return np.array(vectors), all_skills


def cluster_candidates(candidates, n_clusters=3):
    X, all_skills = vectorize_skills(candidates)

    if X.shape[0] < n_clusters:
        n_clusters = max(1, X.shape[0] // 2)  # evitar error con pocos datos

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X)

    return {
        "clusters": labels.tolist(),
        "skills": all_skills,
        "centroids": kmeans.cluster_centers_.tolist()
    }
