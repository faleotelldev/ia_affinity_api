# app/models/job.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base


class Job(Base):
    __tablename__ = "jobs"   # dbo.jobs

    id = Column("id", Integer, primary_key=True, index=True)
    title = Column("title", String(255), nullable=False)
    description = Column("description", String(2000), nullable=True)
    location = Column("location", String(255), nullable=True)
    salary_from = Column("salary_from", Integer, nullable=True)
    salary_to = Column("salary_to", Integer, nullable=True)
    created_at = Column("created_at", DateTime(timezone=True), nullable=True, default=datetime.utcnow)
    updated_at = Column("updated_at", DateTime(timezone=True), nullable=True)
