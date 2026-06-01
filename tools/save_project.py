import originpro as op
from pathlib import Path

def save_project(path: str):
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    op.save(str(out))
    return str(out)
