"""Mock mode: loads sample jobs, matches, and emails so the app works with no credentials."""
from __future__ import annotations

import json
from datetime import date, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.config import ROOT_DIR
from backend.models import (ActionStatus, ApplicationStatus, EmailAction, EmailCategory,
                            EmailMessage, JobApplication, JobMatch)
from backend.schemas import JobMatchSchema, JobSchema
from repositories.job_repository import upsert_job

DATA = ROOT_DIR / "data"


def load_sample_profile() -> dict:
    return json.loads((DATA / "sample_resume_profile.json").read_text())


def load_mock_data(session: Session, user_id: int) -> dict[str, int]:
    """Idempotent: running twice adds nothing new."""
    added = {"jobs": 0, "emails": 0}
    for raw in json.loads((DATA / "mock_jobs.json").read_text()):
        demo = raw.pop("_demo_match")
        raw["posted_at"] = date.fromisoformat(raw["posted_at"])
        job, created = upsert_job(session, JobSchema(**raw))
        added["jobs"] += int(created)
        if not session.scalar(select(JobMatch).where(JobMatch.user_id == user_id, JobMatch.job_id == job.id)):
            m = JobMatchSchema(**demo)
            session.add(JobMatch(user_id=user_id, job_id=job.id, score=m.score,
                                 matching_skills=m.matching_skills, missing_skills=m.missing_skills,
                                 eligibility_concerns=m.eligibility_concerns, explanation=m.explanation,
                                 recommended_action=m.recommended_action))
        if job.company == "Northwind Labs" and not session.scalar(
                select(JobApplication).where(JobApplication.user_id == user_id, JobApplication.job_id == job.id)):
            session.add(JobApplication(user_id=user_id, job_id=job.id, status=ApplicationStatus.APPLIED,
                                       applied_at=datetime(2026, 10, 20), next_action="Wait for recruiter reply"))
    session.flush()
    for raw in json.loads((DATA / "mock_emails.json").read_text()):
        if session.scalar(select(EmailMessage).where(EmailMessage.provider_message_id == raw["provider_message_id"])):
            continue
        email = EmailMessage(user_id=user_id, provider_message_id=raw["provider_message_id"], subject=raw["subject"],
                             sender=raw["sender"], received_at=datetime.fromisoformat(raw["received_at"]),
                             category=EmailCategory(raw["category"]), company=raw["company"], role=raw["role"],
                             summary=raw["summary"], web_link=raw["web_link"], snippet=raw["summary"])
        if raw["action"]:
            email.actions.append(EmailAction(action=raw["action"], status=ActionStatus.PENDING,
                                             deadline=date.fromisoformat(raw["deadline"]) if raw["deadline"] else None))
        session.add(email)
        added["emails"] += 1
    session.flush()
    return added
