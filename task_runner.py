import json
from datetime import datetime
from pathlib import Path

import originpro as op

from tools.data_io import load_table, import_to_origin, guess_x, guess_y, guess_all_y
from tools.plotting import plot_line, plot_scatter, plot_column, plot_with_template
from tools.style import apply_style
from tools.exporting import export_graph
from tools.project import save_project
from tools.execute_labtalk import execute as execute_labtalk
from tools.execute_origin_python import execute as execute_origin_python
from tools.analysis import run_analysis
from tools.reporting import write_report

BASE = Path(r"C:\OriginAI\agent")

def log(msg):
    print(msg)
    log_dir = BASE / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    with open(log_dir / "agent.log", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] {msg}\n")

def load_task(path):
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)

def col_index(df, col):
    if isinstance(col, int):
        return col
    return df.columns.get_loc(col)

def normalize_y(df, task, x_name):
    y = task.get("y")

    if y is None:
        if task.get("auto_all_y", True):
            y = guess_all_y(df, x_name)
        else:
            y = [guess_y(df, x_name)]

    if not isinstance(y, list):
        y = [y]

    return y

def infer_plot_type(task):
    if task.get("plot_type"):
        return str(task["plot_type"]).lower()

    goal = str(task.get("goal", "")).lower()

    if "scatter" in goal or "散点" in goal:
        return "scatter"
    if "bar" in goal or "column" in goal or "柱" in goal:
        return "column"

    return "line"

def run_task(task_path):
    task_path = Path(task_path)
    task = load_task(task_path)

    keep_open = task.get("keep_origin_open", True)
    show_origin = task.get("show_origin", True)
    new_project = task.get("new_project", True)

    op.set_show(show_origin)

    if new_project:
        try:
            op.new()
        except Exception:
            pass

    df = None
    wks = None
    graph = None
    outputs = {}

    try:
        if task.get("input_file"):
            log(f"Loading data: {task['input_file']}")
            df = load_table(task["input_file"], task.get("sheet_name", 0))
            wks = import_to_origin(df)

            log("Detected columns:")
            for i, c in enumerate(df.columns):
                log(f"  [{i}] {c}")

        if df is not None and wks is not None and task.get("plot", True):
            x_name = task.get("x") or guess_x(df, task.get("goal", ""))
            y_names = normalize_y(df, task, x_name)

            x_idx = col_index(df, x_name)
            y_idxs = [col_index(df, y) for y in y_names]

            log(f"Selected X: {x_name}")
            log(f"Selected Y: {y_names}")

            template = task.get("template")
            plot_type = infer_plot_type(task)

            if template:
                graph = plot_with_template(wks, template, x_idx, y_idxs)
            elif plot_type == "line":
                graph = plot_line(wks, x_idx, y_idxs)
            elif plot_type == "scatter":
                graph = plot_scatter(wks, x_idx, y_idxs)
            elif plot_type in ["column", "bar"]:
                graph = plot_column(wks, x_idx, y_idxs)
            else:
                raise ValueError(f"Unsupported wrapped plot_type: {plot_type}. Use labtalk/origin_python for custom plots.")

            apply_style(task.get("style", "default"))

        if task.get("analysis"):
            log("Running analysis...")
            outputs["analysis"] = run_analysis(task["analysis"], df=df, output_dir=BASE / "outputs")
            outputs["report"] = write_report(outputs["analysis"], BASE / "outputs" / "report.md")

        if task.get("labtalk"):
            log("Running LabTalk...")
            outputs["labtalk"] = execute_labtalk(task["labtalk"])

        if task.get("origin_python"):
            log("Running Origin Python...")
            ctx = {
                "op": op,
                "df": df,
                "wks": wks,
                "graph": graph,
                "outputs": outputs
            }
            execute_origin_python(task["origin_python"], ctx)

        if graph is not None and task.get("export"):
            log("Exporting figures...")
            outputs["figures"] = export_graph(graph, task["export"])

        if task.get("save_project", True):
            project_path = task.get("project_path", str(BASE / "outputs" / "project.opju"))
            outputs["project"] = save_project(project_path)

        log("DONE")
        return outputs

    finally:
        if not keep_open and op.oext:
            op.exit()

if __name__ == "__main__":
    default_task = BASE / "requests" / "demo_task.json"
    result = run_task(default_task)
    print(result)
