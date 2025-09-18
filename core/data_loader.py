import streamlit as st
import pandas as pd
import io

@st.cache_data
def load_csv(uploaded_file):
    """Load uploaded CSV with multiple encodings fallback."""
    try:
        raw = uploaded_file.getvalue()
        for enc in ("utf-8-sig", "utf-8", "latin-1"):
            try:
                return pd.read_csv(io.StringIO(raw.decode(enc)))
            except Exception:
                continue
        raise UnicodeDecodeError("Unable to decode file with utf-8/latin-1.")
    except Exception as e:
        st.error(f"Error reading CSV: {e}")
        return None
