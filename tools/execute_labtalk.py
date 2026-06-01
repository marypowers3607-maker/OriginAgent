import originpro as op

def execute(script: str):
    if not script or not script.strip():
        return None
    print("[LabTalk] Executing...")
    return op.lt_exec(script)
