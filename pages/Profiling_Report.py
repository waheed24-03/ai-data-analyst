import streamlit as st
from ydata_profiling import ProfileReport
import pandas as pd
import time
import io
import base64

# ---------- Streamlit Page Config ----------
st.set_page_config(
    layout="wide",
    page_title="Profiling Report",
    page_icon="📊"
)

st.title("📊 Dataset Profiling Report")

# ---------- Sidebar ----------
with st.sidebar:
    if st.button("🏠 Go to Home Page"):
        st.session_state.show_home = True
        st.rerun()

# ---------- CSV Selection ----------
st.subheader("Select Dataset")

# Option 1: Upload CSV
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.session_state.df = df
    st.session_state.file_name = uploaded_file.name
    st.success(f"✅ Loaded {uploaded_file.name} ({df.shape[0]} rows, {df.shape[1]} columns)")

# Option 2: Use CSV from app page 
elif st.session_state.get("df") is not None:
    df = st.session_state.df
    st.info(f"Using previously loaded CSV: {st.session_state.get('file_name', 'dataset')} ({df.shape[0]} rows, {df.shape[1]} columns)")
else:
    st.info("Please upload a CSV file or load one from the main app.")
    st.stop()

# ---------- Load Profiling Button ----------
if st.button("Load the Profile"):
    st.session_state.load_profile = True
    st.rerun()

# ---------- Generate Profiling Report ----------
if st.session_state.get("load_profile"):
    with st.spinner("⏳ Generating Profiling Report..."):
        start_time = time.time()
        progress = st.progress(0)
        status_text = st.empty()

        # Fake progress for UI
        for percent in range(0, 50, 10):
            time.sleep(0.1)
            progress.progress(percent)
            status_text.text(f"Initializing... {percent}%")

        try:
            profile = ProfileReport(
                df,
                title="Profiling Report",
                explorative=True,
                html={"style": {"theme": "cosmo"}}
            )
            html_report = profile.to_html()

            elapsed_time = time.time() - start_time
            progress.progress(100)
            status_text.text(f"✅ Done in {elapsed_time:.1f} seconds!")

            # ---------- Download HTML as PDF  ----------
            pdf_buffer = io.BytesIO()
            pdf_buffer.write(html_report.encode('utf-8'))
            pdf_buffer.seek(0)

            # Download button above the report
            st.download_button(
                label="📥 Download Profiling Report",
                data=pdf_buffer,
                file_name=f"Profiling_Report_{st.session_state.get('file_name','dataset')}.html",
                mime="text/html"
            )

            # ---------- Show report in Streamlit ----------
            st.components.v1.html(html_report, height=800, scrolling=True)

        except Exception as e:
            st.error(f"❌ Could not generate the profiling report. Error: {e}")
