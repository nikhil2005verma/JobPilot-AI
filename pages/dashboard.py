import plotly.express as px
import streamlit as st

from repositories.stats_repo import dashboard_stats, status_breakdown

st.title("🏠 Home Dashboard")
st.caption("Resume upload karo, jobs dhundo, applications track karo — sab ek jagah.")

s = dashboard_stats()
cols = st.columns(5)
cols[0].metric("Jobs discovered", s["total_jobs"])
cols[1].metric("High-match jobs", s["high_match"])
cols[2].metric("Applications tracked", s["applications"])
cols[3].metric("Pending registrations", s["pending_registrations"])
cols[4].metric("Upcoming interviews", s["interviews"])

st.subheader("Application pipeline")
data = status_breakdown()
if data:
    fig = px.bar(x=list(data.keys()), y=list(data.values()), labels={"x": "Status", "y": "Count"})
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Abhi koi application nahi hai. Phase 2 mein resume upload se start karenge.")
