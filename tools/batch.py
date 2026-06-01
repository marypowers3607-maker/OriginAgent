from pathlib import Path


def build_batch_tasks(batch_config, task_template):
    if not batch_config:
        return []

    folder = Path(batch_config.get("folder", "."))
    pattern = batch_config.get("pattern", "*")
    files = sorted(folder.glob(pattern))
    tasks = []

    for file_path in files:
        task = dict(task_template)
        task.pop("batch", None)
        task["input_file"] = str(file_path).replace("\\", "/")
        tasks.append(task)

    return tasks


def scan_files(folder, pattern="*"):
    return [str(path).replace("\\", "/") for path in sorted(Path(folder).glob(pattern))]
