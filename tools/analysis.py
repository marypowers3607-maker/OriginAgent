from pathlib import Path

import numpy as np
import pandas as pd

from tools.execute_labtalk import execute as execute_labtalk


def run_analysis(analysis, df=None, output_dir=None):
    if not analysis:
        return None

    output_dir = Path(output_dir or r"C:\OriginAI\agent\outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    if isinstance(analysis, list):
        return [run_analysis(item, df=df, output_dir=output_dir) for item in analysis]

    if isinstance(analysis, str):
        analysis_type = analysis.lower()
        params = {}
    else:
        analysis_type = str(analysis.get("type", "")).lower()
        params = analysis.get("params", {}) or {}

    if analysis_type in ["none", ""]:
        return None

    if analysis_type == "custom_labtalk":
        return {
            "type": analysis_type,
            "script": params.get("script", ""),
            "result": execute_labtalk(params.get("script", "")),
        }

    if df is None:
        raise ValueError(f"Analysis '{analysis_type}' requires input data")

    if analysis_type == "statistics":
        return _statistics(df)
    if analysis_type == "linear_fit":
        return _linear_fit(df, params)
    if analysis_type == "peak_analysis":
        return _peak_analysis(df, params)
    if analysis_type == "fft":
        return _fft(df, params, output_dir)
    if analysis_type == "pca":
        return _pca(df, output_dir)

    raise NotImplementedError(
        f"Analysis '{analysis_type}' is not supported. "
        "Use task.labtalk, task.origin_python, or analysis.type='custom_labtalk' for custom commands."
    )


def _numeric_series(df, column, role):
    if column is None:
        raise ValueError(f"Missing {role} column")
    if column not in df.columns:
        raise ValueError(f"{role} column not found: {column}")
    return pd.to_numeric(df[column], errors="coerce")


def _xy_data(df, params):
    x_name = params.get("x")
    y_name = params.get("y")
    x = _numeric_series(df, x_name, "x")
    y = _numeric_series(df, y_name, "y")
    data = pd.DataFrame({"x": x, "y": y}).dropna()
    if data.empty:
        raise ValueError("No numeric x/y data available after dropping missing values")
    return x_name, y_name, data["x"].to_numpy(dtype=float), data["y"].to_numpy(dtype=float)


def _statistics(df):
    table = df.describe()
    return {
        "type": "statistics",
        "describe": table,
    }


def _linear_fit(df, params):
    x_name, y_name, x, y = _xy_data(df, params)
    if len(x) < 2:
        raise ValueError("linear_fit requires at least two valid data points")

    slope, intercept = np.polyfit(x, y, 1)
    predicted = slope * x + intercept
    ss_res = float(np.sum((y - predicted) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r2 = 1.0 if ss_tot == 0 else 1.0 - ss_res / ss_tot

    return {
        "type": "linear_fit",
        "x": x_name,
        "y": y_name,
        "slope": float(slope),
        "intercept": float(intercept),
        "r2": float(r2),
        "n": int(len(x)),
    }


def _peak_analysis(df, params):
    x_name, y_name, x, y = _xy_data(df, params)
    if len(y) < 3:
        peaks = np.array([], dtype=int)
        method = "too_few_points"
    else:
        try:
            from scipy.signal import find_peaks

            peaks, _ = find_peaks(y)
            method = "scipy.signal.find_peaks"
        except Exception:
            peaks = _local_maxima(y)
            method = "local_maxima_fallback"

    peak_table = pd.DataFrame(
        {
            "index": peaks.astype(int),
            x_name: x[peaks] if len(peaks) else [],
            y_name: y[peaks] if len(peaks) else [],
        }
    )

    return {
        "type": "peak_analysis",
        "x": x_name,
        "y": y_name,
        "method": method,
        "peak_count": int(len(peaks)),
        "peaks": peak_table,
    }


def _local_maxima(y):
    indexes = []
    for i in range(1, len(y) - 1):
        if y[i] > y[i - 1] and y[i] > y[i + 1]:
            indexes.append(i)
    return np.array(indexes, dtype=int)


def _fft(df, params, output_dir):
    x_name, y_name, x, y = _xy_data(df, params)
    if len(x) < 2:
        raise ValueError("fft requires at least two valid data points")

    order = np.argsort(x)
    x = x[order]
    y = y[order] - np.mean(y)

    dx = np.diff(x)
    sample_spacing = float(np.median(dx)) if len(dx) else 1.0
    if sample_spacing <= 0:
        raise ValueError("fft requires increasing x values")

    freq = np.fft.rfftfreq(len(y), d=sample_spacing)
    amplitude = np.abs(np.fft.rfft(y)) / len(y)
    if len(amplitude) > 1:
        amplitude[1:] *= 2

    spectrum = pd.DataFrame({"frequency": freq, "amplitude": amplitude})
    csv_path = output_dir / "fft_result.csv"
    spectrum.to_csv(csv_path, index=False)

    search = amplitude.copy()
    if len(search) > 1:
        search[0] = 0
    dominant_index = int(np.argmax(search))

    return {
        "type": "fft",
        "x": x_name,
        "y": y_name,
        "sample_spacing": sample_spacing,
        "dominant_frequency": float(freq[dominant_index]),
        "dominant_amplitude": float(amplitude[dominant_index]),
        "spectrum": spectrum,
        "csv": str(csv_path),
    }


def _pca(df, output_dir):
    numeric = df.select_dtypes(include="number").copy()
    if numeric.empty:
        raise ValueError("pca requires at least one numeric column")

    numeric = numeric.dropna()
    if numeric.empty:
        raise ValueError("pca has no complete numeric rows after dropping missing values")

    centered = numeric - numeric.mean(axis=0)
    values = centered.to_numpy(dtype=float)
    u, singular_values, vt = np.linalg.svd(values, full_matrices=False)

    scores = u * singular_values
    components = [f"PC{i + 1}" for i in range(len(singular_values))]
    scores_df = pd.DataFrame(scores, columns=components, index=numeric.index)
    loadings_df = pd.DataFrame(vt.T, index=numeric.columns, columns=components)

    denom = max(len(values) - 1, 1)
    explained_variance = (singular_values ** 2) / denom
    total = float(np.sum(explained_variance))
    explained_ratio = explained_variance / total if total else np.zeros_like(explained_variance)

    scores_path = output_dir / "pca_scores.csv"
    loadings_path = output_dir / "pca_loadings.csv"
    scores_df.to_csv(scores_path, index_label="row")
    loadings_df.to_csv(loadings_path, index_label="variable")

    return {
        "type": "pca",
        "columns": list(numeric.columns),
        "n_rows": int(len(numeric)),
        "singular_values": [float(v) for v in singular_values],
        "explained_variance": [float(v) for v in explained_variance],
        "explained_variance_ratio": [float(v) for v in explained_ratio],
        "scores_csv": str(scores_path),
        "loadings_csv": str(loadings_path),
        "scores": scores_df,
        "loadings": loadings_df,
    }
