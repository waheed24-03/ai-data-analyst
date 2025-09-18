# core/keyword_extractor.py

import pandas as pd
import numpy as np

def select_important_features(df: pd.DataFrame, max_cols: int = 15):
    """
    Analyzes the dataframe and selects the most important columns for analysis.

    Args:
        df (pd.DataFrame): The input dataframe.
        max_cols (int): The maximum number of important columns to return.

    Returns:
        list: A list of the most informative column names.
    """
    if df.empty:
        return []

    # 1. Calculate scores for numeric columns (based on standard deviation)
    numeric_cols = df.select_dtypes(include=np.number)
    # Normalize std dev by mean to handle different scales (Coefficient of Variation)
    # Add a small epsilon to avoid division by zero
    numeric_scores = numeric_cols.std() / (numeric_cols.mean().abs() + 1e-10)
    
    # 2. Calculate scores for categorical columns (based on cardinality)
    categorical_cols = df.select_dtypes(include=['object', 'category'])
    categorical_scores = {}
    for col in categorical_cols.columns:
        num_unique = df[col].nunique()
        # Ignore high-cardinality (like IDs) and single-value columns
        if 1 < num_unique < 50:
            # We just give it a score of 1 to be included, could be more complex
            categorical_scores[col] = 1 

    # Convert scores to pandas Series for easy sorting
    numeric_scores = numeric_scores.sort_values(ascending=False)
    categorical_scores = pd.Series(categorical_scores).sort_values(ascending=False)

    # 3. Combine and select the top columns
    important_numeric = numeric_scores.head(max_cols // 2).index.tolist()
    important_categorical = categorical_scores.head(max_cols - len(important_numeric)).index.tolist()
    
    important_cols = important_numeric + important_categorical
    
    # If we still have no columns, fall back to just taking a sample
    if not important_cols:
        important_cols = df.columns.tolist()[:max_cols]
        
    return important_cols[:max_cols]