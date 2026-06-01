from pathlib import Path
import pandas as pd
import originpro as op

def load_table(path: str, sheet_name=0):
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Data file not found: {p}")

    suffix = p.suffix.lower()

    if suffix in [".xlsx", ".xls"]:
        df = pd.read_excel(p, sheet_name=sheet_name)
    elif suffix in [".csv"]:
        df = pd.read_csv(p)
    elif suffix in [".txt", ".dat"]:
        df = pd.read_csv(p, sep=None, engine="python")
    else:
        raise ValueError(f"Unsupported data format: {suffix}")

    if df.empty:
        raise ValueError("Loaded data is empty")

    return df

def import_to_origin(df):
    wks = op.new_sheet()
    wks.from_df(df)
    return wks

def guess_x(df, goal=""):
    cols = list(df.columns)
    numeric = list(df.select_dtypes(include="number").columns)

    keys = ["time", "date", "x", "index", "wavelength", "frequency", "freq", "voltage"]
    lower = {str(c).lower(): c for c in cols}

    for key in keys:
        for lc, original in lower.items():
            if key in lc:
                return original

    return numeric[0] if numeric else cols[0]

def guess_y(df, x_col=None):
    numeric = list(df.select_dtypes(include="number").columns)
    candidates = [c for c in numeric if c != x_col]

    if candidates:
        return candidates[0]

    cols = [c for c in df.columns if c != x_col]
    if cols:
        return cols[0]

    raise ValueError("Cannot guess Y column")

def guess_all_y(df, x_col=None):
    numeric = list(df.select_dtypes(include="number").columns)
    ys = [c for c in numeric if c != x_col]

    if ys:
        return ys

    return [c for c in df.columns if c != x_col]
