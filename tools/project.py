from pathlib import Path
import originpro as op

def save_project(path: str):
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    op.save(str(out))
    return str(out)
