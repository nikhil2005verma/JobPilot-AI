"""Read-only dashboard queries."""
from sqlalchemy import func, select

from backend.database import get_session
from backend.models import EmailAction, Job, JobApplication, JobMatch, User


def get_or_create_default_user() -> int:
    with get_session() as s:
        u = s.scalar(select(User).order_by(User.id))
        if not u:
            u = User(name="Local User")
            s.add(u)
            s.flush()
        return u.id


def dashboard_stats() -> dict:
    with get_session() as s:
        return {
            "total_jobs": s.scalar(select(func.count(Job.id))) or 0,
            "high_match": s.scalar(select(func.count(JobMatch.id)).where(JobMatch.score >= 75)) or 0,
            "applications": s.scalar(select(func.count(JobApplication.id))) or 0,
            "pending_registrations": s.scalar(
                select(func.count(JobApplication.id)).where(JobApplication.status == "registration_required")) or 0,
            "interviews": s.scalar(
                select(func.count(JobApplication.id)).where(JobApplication.status == "interview_scheduled")) or 0,
            "pending_email_actions": s.scalar(
                select(func.count(EmailAction.id)).where(EmailAction.status == "pending")) or 0,
        }


def status_breakdown() -> dict[str, int]:
    with get_session() as s:
        rows = s.execute(select(JobApplication.status, func.count()).group_by(JobApplication.status)).all()
        return {k: v for k, v in rows}
