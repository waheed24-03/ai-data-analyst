import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import hashlib, os, logging

from core.llm_client import get_llm, generate_python_code
from core.executor import execute_code
from utils.schema import generate_profiling_summary
from core.export_utils import export_csv, export_plots, export_pdf
from core.chat_memory import load_chat_history, append_chat, save_chat_history

# ---------- Logging ----------
logging.basicConfig(filename="analysis.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# ---------- Paths ----------
UPLOAD_DIR = os.path.join("chat_history", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ---------- Streamlit config ----------
st.set_page_config(page_title="AI Co-Pilot Visualization", page_icon="🧑‍💻", layout="wide")
st.title("AI Co-Pilot Visualization 🧑‍💻")

# ---------- Sidebar: Chat + Navigation ----------
with st.sidebar:
    st.header("Chats")
    if st.session_state.get("file_id"):
        history = load_chat_history(st.session_state.file_id)
        if history:
            for i, chat in enumerate(reversed(history)):
                # --- CORRECTED LINE ---
                st.button(
                    label=chat['query'][:60] + "...",
                    key=f"chat_btn_{st.session_state.file_id}_{i}",
                    width='stretch', # <-- Use 'width' instead of 'use_container_width'
                    help=f"Q: {chat['query']}\n\nA: {chat['response']}"
                )
            # --- CORRECTED LINE ---
            if st.button("🗑️ Clear Chat History", width='stretch'): # <-- Use 'width' instead of 'use_container_width'
                save_chat_history(st.session_state.file_id, [])
                st.rerun() 
        else:
            st.info("No chats for this dataset yet.")
    else:
        st.info("Upload a dataset to start.")

    st.markdown("---")
    if st.button("🏠 New Analysis (Home)"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()

# ---------- Upload / Load Dataset ----------
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"], key="analysis_upload")
df, file_id = None, None

if uploaded_file:
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    try:
        df = pd.read_csv(file_path)
        file_id = uploaded_file.name
        st.session_state.df = df
        st.session_state.file_id = file_id
    except Exception as e:
        st.error(f"Failed to load CSV: {e}")
        logging.error(f"CSV load error: {e}")

elif st.button("Load Last Uploaded Dataset"):
    df = st.session_state.get("df")
    file_id = st.session_state.get("file_id")

if df is None or file_id is None:
    st.warning("Please upload a CSV file or load the last uploaded dataset to start.")
    st.stop()

# ---------- Optional Dataset Preview ----------
if st.checkbox("Show Dataset Preview"):
    st.subheader("Dataset Preview")
    st.dataframe(df.head(), width='stretch')

# ---------- Ask for Visualization ----------
user_query = st.text_input("Enter your chart request:", placeholder="e.g., 'Top 5 run scorers'")
visualize_btn = st.button("📈 Visualize")

def ai_chart_suggestion(df, query):
    if "top 5 run scorer" in query.lower() and 'Score A' in df.columns and 'Score B' in df.columns:
        df['Total Runs'] = df['Score A'] + df['Score B']
        top = df.nlargest(5, 'Total Runs')
        fig, ax = plt.subplots(figsize=(8, 5)) 
        ax.bar(top.index.astype(str), top['Total Runs'], color='green')
        ax.set_xlabel('Player Index')
        ax.set_ylabel('Total Runs')
        ax.set_title('Top 5 Run Scorers')
        plt.xticks(rotation=45)
        plt.tight_layout()
        return fig
    return None

# ---------- Handle Visualization ----------
figs, code = [], None

if visualize_btn and user_query:
    try:
        profiling_summary = generate_profiling_summary(df)
        code = generate_python_code(get_llm(), df, user_query, mode="visualize", profiling_summary=profiling_summary)

        exec_result, generated_figs, err = execute_code(code, df)
        if err:
            st.error(f"❌ Execution failed: {err}")
            logging.error(f"Visualization error: {err}")
        else:
            if generated_figs:
                figs.extend(generated_figs)

        suggested_fig = ai_chart_suggestion(df, user_query)
        if suggested_fig:
            figs.append(suggested_fig)

        append_chat(file_id, user_query, "Visualized chart(s)")

        if figs:
            tabs = st.tabs(["Plots", "Generated Code"])
            with tabs[0]:
                st.subheader("Generated Plots")
                for fig in figs:
                    fig.set_size_inches(8, 5) 
                    st.pyplot(fig)

            with tabs[1]:
                if code:
                    st.subheader("Generated Code")
                    st.code(code, language="python")

            st.subheader("Export Options")
            col1, col2, col3 = st.columns(3)
            with col1:
                export_csv(df, label="Download CSV")
            with col2:
                export_plots(figs)
            with col3:
                if st.button("Download PDF Report"):
                    export_pdf(df, summary=None, figs=figs)
        else:
            st.info("No plots were generated for this request.")

    except Exception as e:
        st.error(f"An error occurred: {e}")
        logging.error(f"Unexpected error: {e}")