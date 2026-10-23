from sqlalchemy import create_engine, inspect

from backend import models  # noqa: F401
from backend.config import Settings
from backend.database import Base


def test_all_tables_created():
    eng = create_engine("sqlite://")
    Base.metadata.create_all(eng)
    names = set(inspect(eng).get_table_names())
    assert {"users", "resumes", "resume_profiles", "jobs", "job_matches", "job_applications",
            "email_messages", "email_actions", "user_preferences", "notifications",
            "connected_accounts"} <= names


def test_api_key_not_leaked_in_repr():
    s = Settings(gemini_api_key="secret123")
    assert "secret123" not in repr(s)
    assert s.gemini_configured


def test_missing_key_detected():
    assert not Settings(gemini_api_key="").gemini_configured
