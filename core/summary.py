# In core/summary.py

import streamlit as st
from core.llm_client import get_llm, generate_python_code
from utils.schema import generate_profiling_summary
from core.executor import execute_code

def ai_dataset_summary(df):
    """
    Generates an AI-powered summary of the dataset and RETURNS it as a string.
    """
    try:
        llm = get_llm(model_name="llama3.2:3b")
        profiling_summary = generate_profiling_summary(df)
        
        # A more specific prompt to guide the AI
        prompt = (
            "Based on the provided data profile, write a concise, bulleted summary highlighting "
            "the most important insights about the dataset. Focus on distributions, potential "
            "data quality issues, and key statistics."
        )
        
        code = generate_python_code(
            llm, df, prompt, mode="summarize", profiling_summary=profiling_summary
        )
        
        result, _, err = execute_code(code, df)

        if err:
            return f"Error: Could not generate AI summary.\n\nDetails: {err}"
        elif result:
            return result  # <-- Return the successful result
        else:
            return "Info: The AI ran successfully but did not generate a summary."

    except Exception as e:
        return f"Error: An exception occurred while generating the AI summary: {e}"