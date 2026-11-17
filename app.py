import os
from datetime import datetime, timedelta

import pandas as pd
import streamlit as st

FILE = "data/reports.csv"
STATIONS = ["Chennai Beach", "Guindy", "Chromepet", "Tambaram"]
COACHES = [f"Coach {i}" for i in range(1, 10)]
LEVELS = {1: "Empty", 2: "Few standing", 3: "Full", 4: "Very crowded", 5: "Packed"}

start = datetime(2026, 1, 1, 5, 0)
TIMES = [(start + timedelta(minutes=30 * i)).strftime("%I:%M %p") for i in range(37)]

st.set_page_config(page_title="Chennai Train Crowd Checker", page_icon="🚆")
st.title("Chennai Train Crowd Checker 🚆")


def load():
    if os.path.exists(FILE):
        return pd.read_csv(FILE)
    return pd.DataFrame(columns=["station", "time", "coach", "level"])


tab1, tab2 = st.tabs(["🔍 Get advice", "📝 Report crowd"])

with tab2:
    st.write("Travelled today? Tell us how crowded your coach was.")
    s = st.selectbox("Station", STATIONS, key="rs")
    t = st.selectbox("Time", TIMES, key="rt")
    c = st.selectbox("Coach", COACHES, key="rc")
    lvl = st.select_slider(
        "How crowded?", options=list(LEVELS), format_func=lambda x: f"{x} - {LEVELS[x]}"
    )
    if st.button("Submit report"):
        row = pd.DataFrame([[s, t, c, lvl]], columns=["station", "time", "coach", "level"])
        os.makedirs("data", exist_ok=True)
        pd.concat([load(), row], ignore_index=True).to_csv(FILE, index=False)
        st.success("Thank you! Your report is saved.")

with tab1:
    s2 = st.selectbox("Station", STATIONS, key="as")
    t2 = st.selectbox("Time", TIMES, key="at")
    if st.button("Show advice"):
        df = load()
        d = df[(df.station == s2) & (df.time == t2)]
        if d.empty:
            st.info("No reports yet for this station and time. Use the Report crowd tab to add one!")
        else:
            avg = d.groupby("coach")["level"].mean().round(1)
            best = avg.idxmin()
            st.success(f"Best choice: {best} (crowd level {avg[best]} out of 5)")
            st.bar_chart(avg)
            st.caption(f"Based on {len(d)} real report(s).")
