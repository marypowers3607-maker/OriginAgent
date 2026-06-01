from pathlib import Path

import pandas as pd


def write_report(results, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    blocks = ["# OriginAgent Analysis Report", ""]

    for result in _flatten(results):
        if result is None:
            continue
        blocks.extend(_render_result(result))
        blocks.append("")

    if len(blocks) == 2:
        blocks.extend(["No analysis results.", ""])

    path.write_text("\n".join(blocks), encoding="utf-8")
    return str(path)


def write_error_report(error, traceback_text, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    blocks = [
        "# OriginAgent Analysis Report",
        "",
        "## Error",
        "",
        f"- **Error:** {error}",
        "",
        "### Traceback",
        "",
        "```text",
        traceback_text.rstrip(),
        "```",
        "",
    ]
    path.write_text("\n".join(blocks), encoding="utf-8")
    return str(path)


def _flatten(results):
    if isinstance(results, list):
        for item in results:
            yield from _flatten(item)
    else:
        yield results


def _render_result(result):
    result_type = result.get("type", "analysis")
    lines = [f"## {result_type}", ""]

    for key, value in result.items():
        if key == "type":
            continue
        lines.extend(_render_value(key, value))

    return lines


def _render_value(key, value):
    title = key.replace("_", " ").title()

    if isinstance(value, pd.DataFrame):
        return [f"### {title}", "", _df_to_markdown(value), ""]

    if isinstance(value, pd.Series):
        return [f"### {title}", "", _df_to_markdown(value.to_frame()), ""]

    if isinstance(value, dict):
        rows = [(k, v) for k, v in value.items()]
        return [f"### {title}", "", _df_to_markdown(pd.DataFrame(rows, columns=["key", "value"]), index=False), ""]

    if isinstance(value, list):
        if value and all(not isinstance(item, (dict, list, tuple)) for item in value):
            rows = [(i + 1, item) for i, item in enumerate(value)]
            return [f"### {title}", "", _df_to_markdown(pd.DataFrame(rows, columns=["index", "value"]), index=False), ""]
        return [f"### {title}", "", "```json", str(value), "```", ""]

    return [f"- **{title}:** {value}"]


def _df_to_markdown(df, index=True):
    table = df.reset_index() if index else df.copy()
    columns = [str(col) for col in table.columns]
    rows = []

    for _, row in table.iterrows():
        rows.append([_format_cell(row[col]) for col in table.columns])

    header = "| " + " | ".join(_escape_cell(col) for col in columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(_escape_cell(cell) for cell in row) + " |" for row in rows]
    return "\n".join([header, separator] + body)


def _format_cell(value):
    if pd.isna(value):
        return ""
    if isinstance(value, float):
        return f"{value:.6g}"
    return str(value)


def _escape_cell(value):
    return str(value).replace("|", "\\|").replace("\n", " ")
