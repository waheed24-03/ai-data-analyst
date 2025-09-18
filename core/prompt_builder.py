# core/prompt_builder.py
import textwrap
import pandas as pd
from utils.schema import dataframe_schema_str

# --- UPDATED FUNCTION ---
def build_prompt(df: pd.DataFrame, user_query: str, mode: str, profiling_summary: str) -> str:
    """
    Builds the prompt for the LLM, now including a profiling summary for better context.
    """
    schema = dataframe_schema_str(df)
    
    if mode == "visualize":
        task = (
            "Write plotting code using matplotlib. Use df/pd/np/plt. "
            "If counting or grouping, create matching length Series/lists for x and y, then plot them. "
            "You may also set a `result` variable with a short textual answer."
        )
    elif mode == "summarize":
        task = (
            "Write Python code for a concise textual summary relevant to the user's question. "
            "Assign this summary string to a variable named `result`."
        )
    else: # analyze
        task = (
            "Compute or extract the requested information using pandas. "
            "If the user asks 'which' or 'what', return the corresponding name/value (not just a number). "
            "Assign the final value to a variable named `result`."
        )

    # --- UPDATED PROMPT STRING ---
    return textwrap.dedent(f"""
    You are an expert Python data analyst. Your task is to write a Python script to answer the user's question about a DataFrame named `df`.

    **DataFrame Schema:**
    ```
    {schema}
    ```

    **Key Data Summary & Statistics:**
    ```
    {profiling_summary}
    ```

    **User question:**
    {user_query}

    **INSTRUCTIONS:**
    1) Based on the user's question and the data summary, {task}
    2) DO NOT include any import statements.
    3) Your final answer MUST be assigned to the `result` variable.
    4) Return ONLY the Python code inside a single markdown ```python ... ``` block. No other text.
    """)