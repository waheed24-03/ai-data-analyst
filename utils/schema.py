import pandas as pd

def dataframe_schema_str(df: pd.DataFrame) -> str:
    buf = [f"Rows: {len(df)}", "Columns:"]
    for col in df.columns:
        dtype = str(df[col].dtype)
        non_null_vals = df[col].dropna()
        sample = repr(non_null_vals.iloc[0]) if len(non_null_vals) > 0 else "None"
        buf.append(f" - {col} ({dtype}), example: {sample}")
    return "\n".join(buf)



# --- New: lightweight profiling summary ---
def generate_profiling_summary(df: pd.DataFrame) -> str:
    """
    Returns a summary string including:
    - Number of rows / columns
    - Column names and types
    - Top 3 unique values per categorical column
    - Basic stats for numeric columns
    """
    summary = [f"Dataset has {df.shape[0]} rows and {df.shape[1]} columns."]
    
    # Column info
    for col in df.columns:
        dtype = str(df[col].dtype)
        summary.append(f"- {col} ({dtype})")
        
        if pd.api.types.is_numeric_dtype(df[col]):
            summary.append(f"  * min: {df[col].min()}, max: {df[col].max()}, mean: {df[col].mean():.2f}")
        elif pd.api.types.is_object_dtype(df[col]):
            top_vals = df[col].value_counts().head(3)
            top_str = ", ".join([f"{v} ({c})" for v, c in zip(top_vals.index, top_vals.values)])
            summary.append(f"  * top values: {top_str}")
    
    return "\n".join(summary)
