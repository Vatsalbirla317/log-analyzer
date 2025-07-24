import streamlit as st

# ✅ Page config must come FIRST
st.set_page_config(page_title="Log Analyzer", layout="wide")

import pandas as pd
from utils.parser import parse_log_file
from utils.anomaly import detect_anomalies
from utils.storage import init_db, save_logs  # updated here
from streamlit_autorefresh import st_autorefresh

init_db()  # ⬅️ added this to ensure table is created


# 🔁 Auto-refresh every 10 seconds
st_autorefresh(interval=10_000, limit=None, key="refresh")

st.title("📊 Log Analyzer Dashboard")

# --- Upload log file ---
uploaded_file = st.file_uploader("Upload a log file (.log or .json)", type=["log", "json"])

if uploaded_file:
    content = uploaded_file.read().decode("utf-8")
    with open("logs/temp_uploaded.log", "w") as f:
        f.write(content)
    df = parse_log_file("logs/temp_uploaded.log")
    st.success("✅ File uploaded and parsed successfully!")
else:
    df = parse_log_file("logs/sample1.log")

# --- Filter logs ---
st.subheader("🔍 Filter Logs")
services = ['All'] + sorted(df['service'].unique())
levels = ['All'] + sorted(df['level'].unique())

col1, col2 = st.columns(2)
selected_service = col1.selectbox("Service", services)
selected_level = col2.selectbox("Log Level", levels)

if selected_service != 'All':
    df = df[df['service'] == selected_service]
if selected_level != 'All':
    df = df[df['level'] == selected_level]

# --- Show parsed logs ---
st.subheader("🧾 Parsed Logs")
st.dataframe(df)

# --- Save to DB ---
if st.button("💾 Save logs to DB"):
    save_logs(df)
    st.success("Logs saved to SQLite!")

# --- Anomaly detection ---
st.subheader("🚨 Anomalous Services")
anomalies = detect_anomalies(df)

if anomalies.empty:
    st.success("No anomalies detected 🎉")
else:
    st.error("Anomalies found!")
    st.dataframe(anomalies)

    # Simulated alert
    st.warning("📢 Alert: Spike in anomalies detected!")
    print("⚠️ SLACK ALERT: Spike detected in services:", anomalies['service'].tolist())

# --- Error chart ---
st.subheader("📈 Error Count by Service")
error_counts = df[df['level'] == 'ERROR'].groupby('service').size()
if not error_counts.empty:
    st.bar_chart(error_counts)
else:
    st.info("No error logs to display.")
