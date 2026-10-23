"""All 11 database models with relationships, timestamps, constraints, indexes."""
from datetime import datetime, timezone

from sqlalchemy import (JSON, Boolean, DateTime, Float, ForeignKey, Index, Integer, String, Text,
                        UniqueConstraint)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, onupdate=utcnow)


class User(Base, TimestampMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), default="Local User")
    email: Mapped[str | None] = mapped_column(String(255), unique=True)
    resumes = relationship("Resume", back_populates="user", cascade="all, delete-orphan")
    preference = relationship("UserPreference", back_populates="user", uselist=False, cascade="all, delete-orphan")
    applications = relationship("JobApplication", back_populates="user", cascade="all, delete-orphan")
    accounts = relationship("ConnectedAccount", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")


class Resume(Base, TimestampMixin):
    __tablename__ = "resumes"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    filename: Mapped[str] = mapped_column(String(255))
    file_hash: Mapped[str] = mapped_column(String(64))
    raw_text: Mapped[str] = mapped_column(Text)
    user = relationship("User", back_populates="resumes")
    profile = relationship("ResumeProfile", back_populates="resume", uselist=False, cascade="all, delete-orphan")
    __table_args__ = (UniqueConstraint("user_id", "file_hash", name="uq_resume_user_hash"),)


class ResumeProfile(Base, TimestampMixin):
    __tablename__ = "resume_profiles"
    id: Mapped[int] = mapped_column(primary_key=True)
    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.id", ondelete="CASCADE"), unique=True)
    data: Mapped[dict] = mapped_column(JSON, default=dict)  # skills, education, roles, ...
    user_edited: Mapped[bool] = mapped_column(Boolean, default=False)
    resume = relationship("Resume", back_populates="profile")


class Job(Base, TimestampMixin):
    __tablename__ = "jobs"
    id: Mapped[int] = mapped_column(primary_key=True)
    fingerprint: Mapped[str] = mapped_column(String(64), unique=True)  # dedupe key
    source: Mapped[str] = mapped_column(String(50), index=True)
    title: Mapped[str] = mapped_column(String(255), index=True)
    company: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[str] = mapped_column(Text, default="")
    required_skills: Mapped[list] = mapped_column(JSON, default=list)
    location: Mapped[str | None] = mapped_column(String(255))
    work_mode: Mapped[str | None] = mapped_column(String(30))
    experience: Mapped[str | None] = mapped_column(String(100))
    salary: Mapped[str | None] = mapped_column(String(100))
    posted_at: Mapped[datetime | None] = mapped_column(DateTime)
    url: Mapped[str] = mapped_column(String(1000))
    application_instructions: Mapped[str | None] = mapped_column(Text)
    matches = relationship("JobMatch", back_populates="job", cascade="all, delete-orphan")
    applications = relationship("JobApplication", back_populates="job", cascade="all, delete-orphan")


class JobMatch(Base, TimestampMixin):
    __tablename__ = "job_matches"
    id: Mapped[int] = mapped_column(primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id", ondelete="CASCADE"))
    resume_profile_id: Mapped[int] = mapped_column(ForeignKey("resume_profiles.id", ondelete="CASCADE"))
    score: Mapped[float] = mapped_column(Float, index=True)
    matching_skills: Mapped[list] = mapped_column(JSON, default=list)
    missing_skills: Mapped[list] = mapped_column(JSON, default=list)
    concerns: Mapped[list] = mapped_column(JSON, default=list)
    explanation: Mapped[str | None] = mapped_column(Text)
    next_action: Mapped[str | None] = mapped_column(String(255))
    job = relationship("Job", back_populates="matches")
    __table_args__ = (UniqueConstraint("job_id", "resume_profile_id", name="uq_match_job_profile"),)


class JobApplication(Base, TimestampMixin):
    __tablename__ = "job_applications"
    STATUSES = ["shortlisted", "applied", "registration_required", "interview_scheduled", "rejected", "offer_received"]
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id", ondelete="CASCADE"))
    status: Mapped[str] = mapped_column(String(30), default="shortlisted", index=True)
    applied_at: Mapped[datetime | None] = mapped_column(DateTime)
    next_action: Mapped[str | None] = mapped_column(String(255))
    follow_up_at: Mapped[datetime | None] = mapped_column(DateTime)
    notes: Mapped[str | None] = mapped_column(Text)
    cover_letter: Mapped[str | None] = mapped_column(Text)
    user = relationship("User", back_populates="applications")
    job = relationship("Job", back_populates="applications")
    emails = relationship("EmailMessage", back_populates="application")
    __table_args__ = (UniqueConstraint("user_id", "job_id", name="uq_application_user_job"),)


class ConnectedAccount(Base, TimestampMixin):
    __tablename__ = "connected_accounts"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    provider: Mapped[str] = mapped_column(String(30))
    account_email: Mapped[str] = mapped_column(String(255))
    encrypted_token: Mapped[str | None] = mapped_column(Text)  # encrypted, never plaintext
    consent_given_at: Mapped[datetime | None] = mapped_column(DateTime)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime)
    user = relationship("User", back_populates="accounts")
    __table_args__ = (UniqueConstraint("user_id", "provider", "account_email", name="uq_account"),)


class EmailMessage(Base, TimestampMixin):
    __tablename__ = "email_messages"
    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("connected_accounts.id", ondelete="CASCADE"), index=True)
    application_id: Mapped[int | None] = mapped_column(ForeignKey("job_applications.id", ondelete="SET NULL"))
    provider_message_id: Mapped[str] = mapped_column(String(255))
    subject: Mapped[str] = mapped_column(String(500))
    sender: Mapped[str] = mapped_column(String(255))
    received_at: Mapped[datetime] = mapped_column(DateTime, index=True)
    category: Mapped[str | None] = mapped_column(String(40), index=True)
    summary: Mapped[str | None] = mapped_column(Text)
    web_link: Mapped[str | None] = mapped_column(String(1000))
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    application = relationship("JobApplication", back_populates="emails")
    actions = relationship("EmailAction", back_populates="email", cascade="all, delete-orphan")
    __table_args__ = (UniqueConstraint("account_id", "provider_message_id", name="uq_email_provider_id"),)


class EmailAction(Base, TimestampMixin):
    __tablename__ = "email_actions"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_id: Mapped[int] = mapped_column(ForeignKey("email_messages.id", ondelete="CASCADE"), index=True)
    company: Mapped[str | None] = mapped_column(String(255))
    role: Mapped[str | None] = mapped_column(String(255))
    action_required: Mapped[str | None] = mapped_column(String(500))
    deadline: Mapped[datetime | None] = mapped_column(DateTime)
    official_link: Mapped[str | None] = mapped_column(String(1000))
    status: Mapped[str] = mapped_column(String(20), default="pending", index=True)
    email = relationship("EmailMessage", back_populates="actions")


class UserPreference(Base, TimestampMixin):
    __tablename__ = "user_preferences"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    preferred_roles: Mapped[list] = mapped_column(JSON, default=list)
    preferred_locations: Mapped[list] = mapped_column(JSON, default=list)
    experience_level: Mapped[str] = mapped_column(String(30), default="Fresher")
    remote_only: Mapped[bool] = mapped_column(Boolean, default=False)
    notify_new_matches: Mapped[bool] = mapped_column(Boolean, default=True)
    search_interval_hours: Mapped[int] = mapped_column(Integer, default=24)
    user = relationship("User", back_populates="preference")


class Notification(Base, TimestampMixin):
    __tablename__ = "notifications"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    kind: Mapped[str] = mapped_column(String(30))
    ref_key: Mapped[str] = mapped_column(String(100))  # e.g. job fingerprint -> no repeat alerts
    message: Mapped[str] = mapped_column(String(500))
    read: Mapped[bool] = mapped_column(Boolean, default=False)
    user = relationship("User", back_populates="notifications")
    __table_args__ = (UniqueConstraint("user_id", "kind", "ref_key", name="uq_notification_once"),
                      Index("ix_notification_user_read", "user_id", "read"))
