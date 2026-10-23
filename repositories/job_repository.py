"""All Job / JobMatch database access lives here."""
from __future__ import annotations

import hashlib
import re

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models import Job, JobMatch
from backend.schemas import JobSchema


def _norm(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def job_fingerprint(title: str, company: str, location: str) -> str:
    """Same role posted on two boards (or twice) collapses to one fingerprint."""
    return hashlib.sha256(f"{_norm(title)}|{_norm(company)}|{_norm(location)}".encode()).hexdigest()


def upsert_job(session: Session, data: JobSchema) -> tuple[Job, bool]:
    """Returns (job, created). Existing duplicates are skipped, not overwritten."""
    fp = job_fingerprint(data.title, data.company, data.location)
    existing = session.scalar(select(Job).where(Job.fingerprint == fp))
    if existing:
        return existing, False
    job = Job(fingerprint=fp, **data.model_dump())
    session.add(job)
    session.flush()
    return job, True


def list_jobs_with_scores(session: Session, user_id: int) -> list[tuple[Job, float | None]]:
    rows = session.execute(
        select(Job, JobMatch.score)
        .outerjoin(JobMatch, (JobMatch.job_id == Job.id) & (JobMatch.user_id == user_id))
        .order_by(JobMatch.score.desc().nulls_last(), Job.posted_at.desc().nulls_last())
    ).all()
    return [(j, s) for j, s in rows]
