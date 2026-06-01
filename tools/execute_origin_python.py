import traceback


def execute(code: str, context=None):
    if not code or not code.strip():
        return {
            "status": "skipped",
            "message": "Origin Python code is empty",
        }

    try:
        print("[Origin Python] Executing...")
        ctx = {} if context is None else dict(context)
        exec(code, ctx)
        return {
            "status": "success",
            "context_keys": sorted(k for k in ctx.keys() if not k.startswith("__")),
        }
    except Exception as exc:
        return {
            "status": "error",
            "error": str(exc),
            "traceback": traceback.format_exc(),
        }
