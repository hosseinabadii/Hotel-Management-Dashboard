from pathlib import Path

import streamlit as st

st.set_page_config(page_title="Smart Hotel Management", page_icon=":hotel:", layout="wide")

col1, col2 = st.columns([0.1, 0.9])
with col1:
    st.image(Path(__file__).parent.parent / "images" / "hotel.png")
with col2:
    st.title("Smart Hotel Management")

st.markdown("Welcome to the **Hotel Management System**. Manage customers, rooms, and bookings seamlessly.")

st.divider()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Rooms", "50", "5 new (this month)")
with col2:
    st.metric("Occupancy Rate", "82%", "+3% from last month")
with col3:
    st.metric("Active Bookings", "24", "3 check-ins today")

st.divider()
st.caption("© 2024 Smart Hotel Management | Powered by Streamlit")
