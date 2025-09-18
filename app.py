import streamlit as st
import pandas as pd
import hashlib
import os, json

from core.overrides import intent_override
from core.llm_client import get_llm, generate_python_code
from core.executor import execute_code
from utils.schema import generate_profiling_summary
from core.rag_client import rag_answer
from core.search_client import web_search
from core.summary import ai_dataset_summary
from core.export_utils import export_csv, export_plots, export_pdf
from core.chat_memory import load_chat_history, append_chat, save_chat_history

# ---------- Paths ----------
UPLOAD_DIR = os.path.join("chat_history", "uploads")
os.makedirs("chat_history", exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ---------- Streamlit config ----------
st.set_page_config(page_title="AI Data Analyst", page_icon="🧑‍💻", layout="wide")

# ---------- Helpers ----------
def get_file_hash(uploaded_file):
    return hashlib.md5(uploaded_file.getbuffer()).hexdigest()

def run_rag_or_search(query: str):
    rag_resp = rag_answer(query)
    if rag_resp and "could not find" not in rag_resp.lower() and "don't know" not in rag_resp.lower():
        st.subheader("RAG Answer")
        st.info(rag_resp)
    else:
        with st.spinner("RAG didn’t find an answer. Searching the web... 🌐"):
            search_resp = web_search(query)
            st.subheader("Web Search Answer")
            st.info(search_resp)

# ---------- Main ----------
def main():
    st.title("AI Data Analyst 📈")

    # ---------- CSV Upload in Main Page ----------
    st.subheader("Upload Dataset")
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.session_state.df = df
        st.session_state.file_name = uploaded_file.name
        st.session_state.file_id = get_file_hash(uploaded_file)
        file_path = os.path.join(UPLOAD_DIR, f"{st.session_state.file_id}.csv")
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"✅ Loaded {uploaded_file.name} ({df.shape[0]} rows, {df.shape[1]} columns)")

    # Stop if no dataset uploaded
    if st.session_state.get("df") is None:
        st.info("Please upload a CSV file to start.")
        st.stop()

    df = st.session_state.df
    st.success(f"✅ Data loaded ({df.shape[0]} rows, {df.shape[1]} columns)")

    # ---------- Dataset Preview ----------
    st.dataframe(df.head(), use_container_width=True)

    # ---------- Sidebar: Chats ----------
    with st.sidebar:
        st.subheader("Chats")
        if st.session_state.get("file_id"):
            history = load_chat_history(st.session_state.file_id)
            if history:
                for i, chat in enumerate(reversed(history)):
                    if st.button(chat['query'][:60], key=f"chat_btn_{st.session_state.file_id}_{i}"):
                        st.session_state.last_loaded_query = chat['query']
                        st.session_state.last_loaded_response = chat['response']
                        st.session_state.show_prev_chat = True

            if st.button("🗑️ Clear Chat History"):
                save_chat_history(st.session_state.file_id, [])
                st.session_state.figs = None
                st.session_state.summary_text = None
                st.session_state.result = None
                st.session_state.last_loaded_query = None
                st.session_state.last_loaded_response = None
                st.session_state.show_prev_chat = False
        else:
            st.info("Upload a dataset to start.")

    # ---------- Init session keys ----------
    for key in ['figs', 'summary_text', 'result', 'last_loaded_query', 'last_loaded_response', 'show_prev_chat']:
        if key not in st.session_state:
            st.session_state[key] = None

    # ---------- Ask a Question ----------
    st.header("Ask a Question")
    user_query = st.text_input(
        "Enter your question:",
        placeholder="e.g., 'Which team won the most matches?'",
        value=st.session_state.get("last_loaded_query", "")
    )

    if st.session_state.get("show_prev_chat") and st.session_state.get("last_loaded_response"):
        st.subheader("Previous Chat Response")
        st.write(st.session_state.last_loaded_response)

    col1, col2, col3 = st.columns(3)
    analyze_button = col1.button("📊 Analyze")
    visualize_button = col2.button("📈 Visualize")
    summarize_button = col3.button("📝 Summarize")

    if analyze_button or visualize_button or summarize_button:
        if not user_query and not summarize_button:
            st.warning("Please enter a question to analyze or visualize.")
            st.stop()

        query_to_log = user_query if user_query else "Dataset Summary"
        with st.spinner("The AI is working..."):
            try:
                response_text = ""
                if summarize_button:
                    st.session_state.summary_text = ai_dataset_summary(df)
                    response_text = st.session_state.summary_text
                else:
                    mode = "visualize" if visualize_button else "analyze"
                    code = intent_override(user_query, df, mode) or generate_python_code(
                        get_llm(), df, user_query, mode, generate_profiling_summary(df)
                    )
                    st.subheader("Generated Code")
                    st.code(code, language="python")
                    result, figs, err = execute_code(code, df)

                    if err:
                        st.error(f"❌ Code execution failed: {err}")
                        response_text = f"Error: {err}"
                        run_rag_or_search(user_query)
                    else:
                        st.session_state.result = result
                        st.session_state.figs = figs
                        if result is not None:
                            response_text += str(result)
                        if figs:
                            response_text += f"\n📊 {len(figs)} plot(s) generated."
                        if not response_text:
                            response_text = "Analysis complete with no text output."

                if st.session_state.get("file_id"):
                    append_chat(st.session_state.file_id, query_to_log, response_text)
                    st.session_state.last_loaded_query = None
                    st.session_state.last_loaded_response = None
                    st.session_state.show_prev_chat = False

            except Exception as e:
                st.error(f"An error occurred: {e}")

    # ---------- Display outputs ----------
    if st.session_state.summary_text:
        st.subheader("AI Summary")
        st.write(st.session_state.summary_text)

    if st.session_state.result is not None:
        st.subheader("Result")
        st.write(st.session_state.result)

    if st.session_state.figs:
        st.subheader("Plots")
        for fig in st.session_state.figs:
            st.pyplot(fig)

if __name__ == "__main__":
    main()
