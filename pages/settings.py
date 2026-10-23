import streamlit as st

from backend.config import get_settings

cfg = get_settings()
st.title("⚙️ Settings")

st.subheader("Gemini API")
st.write("API key status:", "✅ configured" if cfg.gemini_configured else "❌ missing (set GEMINI_API_KEY in .env)")
st.write("Model:", f"`{cfg.gemini_model}`")  # key is never displayed
st.write("Mock mode:", "ON (no credentials needed)" if cfg.mock_mode else "OFF")

st.subheader("Storage")
st.write("Database:", cfg.database_url.split("///")[0] + "///…")
st.write("Max upload size:", f"{cfg.max_upload_mb} MB")
st.caption("Preferences, email connection aur data deletion controls aage ke phases mein add honge.")
