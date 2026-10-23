"""Entry point:  streamlit run app.py"""
import streamlit as st

from backend.database import init_db
from repositories.stats_repo import get_or_create_default_user
from utils.logging_utils import setup_logging

st.set_page_config(page_title="AI Job Agent", page_icon="💼", layout="wide")
setup_logging()
init_db()
st.session_state.setdefault("user_id", get_or_create_default_user())

pages = [
    st.Page("pages/dashboard.py", title="Dashboard", icon="🏠", default=True),
    st.Page("pages/resume_analyzer.py", title="Resume Analyzer", icon="📄"),
    st.Page("pages/job_search.py", title="Job Search", icon="🔍"),
    st.Page("pages/recommendations.py", title="Recommended Jobs", icon="⭐"),
    st.Page("pages/email_center.py", title="Email Center", icon="📧"),
    st.Page("pages/application_tracker.py", title="Application Tracker", icon="📋"),
    st.Page("pages/settings.py", title="Settings", icon="⚙️"),
]
st.navigation(pages).run()
