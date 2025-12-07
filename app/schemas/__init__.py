# app/schemas/__init__.py
from .candidate import (
    CandidateBase,
    CandidateCreate,
    CandidateUpdate,
    CandidateRead,
    CandidateMatch,
)
from .job import JobBase, JobCreate, JobUpdate, JobRead, JobMatch
from .analysis_result import (
    AnalysisResultBase,
    AnalysisResultCreate,
    AnalysisResultRead,
)

__all__ = [
    "CandidateBase",
    "CandidateCreate",
    "CandidateUpdate",
    "CandidateRead",
    "CandidateMatch",
    "JobBase",
    "JobCreate",
    "JobUpdate",
    "JobRead",
    "JobMatch",
    "AnalysisResultBase",
    "AnalysisResultCreate",
    "AnalysisResultRead",
]
