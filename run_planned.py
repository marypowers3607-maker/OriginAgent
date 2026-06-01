import sys

from planner import PLANNED_TASK, write_planned_task
from task_runner import run_task


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if not argv:
        print('Usage: py run_planned.py "读取 C:/OriginAI/data/test.xlsx，画 Temperature 随 Time 变化的折线图，做 FFT"')
        return 1

    text = " ".join(argv)
    path, _ = write_planned_task(text, PLANNED_TASK)
    print(f"Planned task written: {path}")
    result = run_task(path)
    print(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
