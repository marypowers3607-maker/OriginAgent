import json
import re
import sys
from pathlib import Path


BASE = Path(r"C:\OriginAI\agent")
PLANNED_TASK = BASE / "requests" / "planned_task.json"


def plan_task(text):
    task = {
        "show_origin": False,
        "keep_origin_open": False,
        "new_project": True,
        "plot": False,
        "style": "science",
        "sheet_name": 0,
        "labtalk": "",
        "origin_python": "",
    }

    input_file = extract_input_file(text)
    if input_file:
        task["input_file"] = input_file

    xy = extract_xy(text)
    if xy:
        task["x"] = xy["x"]
        task["y"] = xy["y"]

    plot_type = extract_plot_type(text)
    if plot_type:
        task["plot"] = True
        task["plot_type"] = plot_type

    analysis = extract_analysis(text, task.get("x"), task.get("y"))
    if analysis:
        task["analysis"] = analysis

    export = extract_export(text)
    if export:
        task["export"] = {"paths": export}

    if has_any(text, ["保存 opju", "保存opju", "save opju"]):
        task["save_project"] = True
        task["project_path"] = str((BASE / "outputs" / "planned_task.opju")).replace("\\", "/")
    else:
        task["save_project"] = False

    if has_any(text, ["生成报告", "report"]):
        task["report"] = True
        task["report_path"] = str((BASE / "outputs" / "report.md")).replace("\\", "/")

    return task


def write_planned_task(text, path=PLANNED_TASK):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    task = plan_task(text)
    path.write_text(json.dumps(task, ensure_ascii=False, indent=2), encoding="utf-8")
    return path, task


def extract_input_file(text):
    match = re.search(r"[A-Za-z]:(?:/|\\)[^\s，,。；;\"']+", text)
    if not match:
        return None
    return match.group(0).rstrip("，,。；;")


def extract_xy(text):
    patterns = [
        r"(?P<y>[A-Za-z_][\w .-]*)\s*随\s*(?P<x>[A-Za-z_][\w .-]*)\s*变化",
        r"以\s*(?P<x>[A-Za-z_][\w .-]*)\s*为\s*X[，,、\s]*(?P<y>[A-Za-z_][\w .-]*)\s*为\s*Y",
        r"(?P<y>[A-Za-z_][\w .-]*)\s+vs\.?\s+(?P<x>[A-Za-z_][\w .-]*)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return {
                "x": clean_column(match.group("x")),
                "y": clean_column(match.group("y")),
            }
    return None


def extract_plot_type(text):
    lower = text.lower()
    if "折线图" in text or "line" in lower:
        return "line"
    if "散点图" in text or "scatter" in lower:
        return "scatter"
    if "柱状图" in text or "column" in lower or "bar" in lower:
        return "column"
    return None


def extract_analysis(text, x=None, y=None):
    candidates = []
    lower = text.lower()

    if "statistics" in lower or "描述性统计" in text:
        candidates.append({"type": "statistics"})
    if "linear fit" in lower or "线性拟合" in text:
        candidates.append(with_xy("linear_fit", x, y))
    if "fft" in lower or "频谱" in text:
        candidates.append(with_xy("fft", x, y))
    if "pca" in lower or "主成分" in text:
        candidates.append({"type": "pca"})
    if "peak" in lower or "峰值" in text:
        candidates.append(with_xy("peak_analysis", x, y))

    if not candidates:
        return None
    if len(candidates) == 1:
        return candidates[0]
    return candidates


def extract_export(text):
    lower = text.lower()
    suffixes = []
    for suffix, keys in [
        ("png", ["png"]),
        ("tif", ["tif", "tiff"]),
        ("pdf", ["pdf"]),
    ]:
        if any(key in lower for key in keys):
            suffixes.append(suffix)

    if not suffixes:
        return []

    return [str((BASE / "outputs" / f"planned_task.{suffix}")).replace("\\", "/") for suffix in suffixes]


def with_xy(analysis_type, x=None, y=None):
    item = {"type": analysis_type}
    if x and y:
        item["params"] = {"x": x, "y": y}
    return item


def has_any(text, phrases):
    lower = text.lower()
    return any(phrase in lower for phrase in phrases)


def clean_column(value):
    return value.strip().strip("，,。；;、 的")


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if not argv:
        print('Usage: py planner.py "读取 C:/OriginAI/data/test.xlsx，画 Temperature 随 Time 变化的折线图，做 FFT"')
        return 1

    text = " ".join(argv)
    path, task = write_planned_task(text)
    print(f"Planned task written: {path}")
    print(json.dumps(task, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
