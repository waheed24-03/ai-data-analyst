import io
import re
import traceback
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from contextlib import redirect_stdout
import multiprocessing

# --- Guardrails: Forbidden Keywords ---
FORBIDDEN_KEYWORDS = [
    "open(", "os.", "sys.", "subprocess", "shutil", "eval", "exec(",
    "import socket", "import requests", "while True", "time.sleep(", "input("
]

def safe_get_first(obj):
    """Safely return the first element of an iterable, else None."""
    try:
        if hasattr(obj, "__len__") and len(obj) > 0:
            if isinstance(obj, pd.Series):
                return obj.iloc[0]
            return obj[0]
    except (IndexError, TypeError):
        return None
    return None

def sanitize_code(code: str) -> str:
    """Removes unsafe imports/keywords and applies robust fixes for unsafe indexing."""
    # 1. Remove standard imports and markdown
    code = re.sub(r'^\s*import\s+[^\n]+', '', code, flags=re.MULTILINE)
    code = re.sub(r'^\s*from\s+[^\n]+\s+import\s+[^\n]+', '', code, flags=re.MULTILINE)
    code = re.sub(r'```', '', code)

    # 2. Check for forbidden keywords
    for kw in FORBIDDEN_KEYWORDS:
        if kw in code:
            raise ValueError(f"Blocked unsafe keyword in code: {kw}")

    # 3. Apply robust line-by-line fixes for unsafe indexing
    fixed_lines = []
    for line in code.splitlines():
        # Fix for .iloc[0]
        if ".iloc[0]" in line:
            line = line.replace(".iloc[0]", ".pipe(safe_get_first)")
        
        # Fix for .unique()[0]
        if ".unique()[0]" in line:
            # Handle assignments correctly by splitting the line
            if "=" in line:
                parts = line.split("=", 1)
                variable_part = parts[0].strip()
                expression_part = parts[1].strip().replace(".unique()[0]", ".unique()")
                line = f"{variable_part} = safe_get_first({expression_part})"
            else:
                expression_part = line.strip().replace(".unique()[0]", ".unique()")
                line = f"result = safe_get_first({expression_part})"
        fixed_lines.append(line)
    
    return "\n".join(fixed_lines)


def _worker(code_to_run, df, return_dict):
    """The function that runs in a separate process to execute code safely."""
    local_env = {
        "__builtins__": {"len": len, "min": min, "max": max, "sum": sum, "sorted": sorted, "range": range, "print": print, "round": round, "enumerate": enumerate, "abs": abs, "zip": zip, "str": str, "int": int, "float": float, "bool": bool, "list": list, "dict": dict},
        "pd": pd, "np": np, "plt": plt, "df": df, "safe_get_first": safe_get_first, "result": None
    }
    
    plt.close("all")
    buf = io.StringIO()
    try:
        with redirect_stdout(buf):
            exec(code_to_run, local_env)
    except Exception:
        return_dict["error"] = traceback.format_exc()
        return

    stdout = buf.getvalue().strip()
    result = local_env.get("result", None)

    if result is None and stdout:
        result = stdout

    figs = [plt.figure(fid) for fid in plt.get_fignums()]

    return_dict["result"] = result
    return_dict["figs"] = figs
    return_dict["error"] = None


def execute_code(code: str, df: pd.DataFrame, timeout: int = 15):
    """Safely execute Python code with the dataframe in a separate process."""
    try:
        code_to_run = sanitize_code(code)
    except ValueError as e:
        return None, None, str(e)

    manager = multiprocessing.Manager()
    return_dict = manager.dict()

    p = multiprocessing.Process(target=_worker, args=(code_to_run, df, return_dict))
    p.start()
    p.join(timeout)

    if p.is_alive():
        p.terminate()
        p.join()
        return None, None, "Execution timed out."

    return return_dict.get("result"), return_dict.get("figs"), return_dict.get("error")