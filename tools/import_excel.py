import pandas as pd
import originpro as op
from pathlib import Path

def import_excel(path: str, sheet_name=0):
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Excel file not found: {file_path}")

    df = pd.read_excel(file_path, sheet_name=sheet_name)

    if df.empty:
        raise ValueError("Excel file is empty")

    wks = op.new_sheet()
    wks.from_df(df)

    return df, wks

def guess_xy_columns(df, goal=""):
    columns = list(df.columns)

    x_keywords = ["time", "date", "x", "index", "wavelength", "frequency"]
    y_keywords = ["temperature", "temp", "value", "signal", "intensity", "response", "y"]

    lower_map = {str(c).lower(): c for c in columns}

    x_col = None
    y_col = None

    for key in x_keywords:
        for lower, original in lower_map.items():
            if key in lower:
                x_col = original
                break
        if x_col is not None:
            break

    for key in y_keywords:
        for lower, original in lower_map.items():
            if key in lower and original != x_col:
                y_col = original
                break
        if y_col is not None:
            break

    numeric_cols = list(df.select_dtypes(include="number").columns)

    if x_col is None:
        if len(numeric_cols) >= 1:
            x_col = numeric_cols[0]
        else:
            x_col = columns[0]

    if y_col is None:
        candidates = [c for c in numeric_cols if c != x_col]
        if candidates:
            y_col = candidates[0]
        elif len(columns) >= 2:
            y_col = columns[1]
        else:
            raise ValueError("Cannot guess Y column: only one column found")

    return x_col, y_col
