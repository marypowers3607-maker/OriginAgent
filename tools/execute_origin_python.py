def execute(code: str, context=None):
    if not code or not code.strip():
        return {}
    print("[Origin Python] Executing...")
    ctx = {} if context is None else dict(context)
    exec(code, ctx)
    return ctx
