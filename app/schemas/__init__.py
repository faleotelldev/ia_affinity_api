# app/schemas/__init__.py
from .candidate import CandidateCreate, CandidateUpdate, CandidateRead
from .job import JobCreate, JobUpdate, JobRead
from .analysis import (
    AnalysisRequest,
    AnalysisResultCreate,
    AnalysisResultRead,
)

__all__ = [
    "CandidateCreate",
    "CandidateUpdate",
    "CandidateRead",
    "JobCreate",
    "JobUpdate",
    "JobRead",
    "AnalysisRequest",
    "AnalysisResultCreate",
    "AnalysisResultRead",
]
