"""Boots every page headlessly; fails on any exception."""
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parent.parent
PAGES = ["dashboard", "resume_analyzer", "job_search", "recommendations",
         "email_center", "application_tracker", "settings"]


@pytest.mark.parametrize("page", PAGES)
def test_page_renders(page, monkeypatch, tmp_path):
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path}/t.db")
    at = AppTest.from_file(str(ROOT / "pages" / f"{page}.py"), default_timeout=30)
    from backend.database import init_db
    init_db()
    at.run()
    assert not at.exception, at.exception
