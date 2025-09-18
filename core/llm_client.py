# core/llm_client.py
import re
import streamlit as st
from core.prompt_builder import build_prompt

def get_llm(model_name: str = "llama3.2:3b", temperature: float = 0.0):
    """Initializes and returns the ChatOllama instance."""
    try:
        from langchain_ollama import ChatOllama
        return ChatOllama(model=model_name, temperature=temperature)
    except ImportError:
        st.error("ChatOllama client not found. Please run: pip install langchain-ollama")
        st.stop()
    except Exception as e:
        st.error(f"Failed to connect to Ollama. Is it running? Error: {e}")
        st.stop()

def extract_code(text: str) -> str:
    """Extracts Python code from a markdown block in a string."""
    # This function is correct, but it requires a string as input.
    match = re.search(r"```(?:python)?\s*([\s\S]*?)```", text)
    return match.group(1).strip() if match else text.strip()

# --- UPDATED FUNCTION ---
def generate_python_code(llm, df, user_query, mode: str, profiling_summary: str) -> str:
    """
    Generates Python code via LLM and correctly extracts the text content
    from the response object before parsing.
    """
    prompt = build_prompt(df, user_query, mode, profiling_summary)
    
    # The llm.invoke() method returns a message object, not a raw string.
    response_obj = llm.invoke(prompt)
    
    # We must extract the string content from the object before processing.
    # The content is usually in the .content attribute.
    if hasattr(response_obj, 'content') and isinstance(response_obj.content, str):
        response_text = response_obj.content
    else:
        # Fallback for other possible response structures
        response_text = str(response_obj)
        
    # Now, we pass the guaranteed string to extract_code.
    return extract_code(response_text)