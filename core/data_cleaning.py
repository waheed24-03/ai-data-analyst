# core/data_cleaning.py
import pandas as pd

def diagnose_data(df: pd.DataFrame) -> dict:
    """Diagnose missing values, duplicate rows, and type mismatches."""
    issues = {}

    # Missing values (percentage of missing across all cells)
    issues['missing_values'] = df.isnull().sum().sum() / (df.shape[0] * df.shape[1])

    # Duplicate rows count
    issues['duplicate_rows'] = df.duplicated().sum()

    # Type mismatches: try to infer
    mismatches = {}
    for col in df.columns:
        if df[col].dtype == object:
            # Try numeric
            coerced_num = pd.to_numeric(df[col], errors='coerce')
            if coerced_num.notnull().sum() > 0 and coerced_num.isnull().sum() > 0:
                mismatches[col] = "numeric"

            # --- UPDATED LINE ---
            # Try date, using format='mixed' for efficiency and to suppress warnings
            coerced_date = pd.to_datetime(df[col], errors='coerce', format='mixed')
            if coerced_date.notnull().sum() > 0 and coerced_date.isnull().sum() > 0:
                mismatches[col] = "datetime"

    issues['type_mismatches'] = mismatches
    return issues


def fix_missing(df: pd.DataFrame, strategy: str = "mean") -> pd.DataFrame:
    """Fix missing values by strategy: mean, median, or fill 'MISSING'."""
    for col in df.columns:
        if df[col].isnull().any():
            if strategy == "mean" and pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].fillna(df[col].mean())
            elif strategy == "median" and pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].fillna(df[col].median())
            else:
                df[col] = df[col].fillna("MISSING")
    return df


def fix_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicate rows."""
    return df.drop_duplicates()


def fix_types(df: pd.DataFrame, mismatches: dict) -> pd.DataFrame:
    """Fix type mismatches by coercion."""
    for col, target_type in mismatches.items():
        if target_type == "numeric":
            df[col] = pd.to_numeric(df[col], errors='coerce')
        elif target_type == "datetime":
            # --- UPDATED LINE ---
            # Also add format='mixed' here for consistency
            df[col] = pd.to_datetime(df[col], errors='coerce', format='mixed')
    return df