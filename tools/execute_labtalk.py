import traceback

import originpro as op


def execute(script: str):
    if not script or not script.strip():
        return {
            "status": "skipped",
            "message": "LabTalk script is empty",
        }

    warning = None
    if "type -b" in script.lower():
        warning = "LabTalk script contains 'type -b', which may show a blocking message box."
        print(f"[LabTalk] WARNING: {warning}")

    try:
        print("[LabTalk] Executing...")
        result = op.lt_exec(script)
        response = {
            "status": "success",
            "result": result,
        }
        if warning:
            response["warning"] = warning
        return response
    except Exception as exc:
        return {
            "status": "error",
            "error": str(exc),
            "traceback": traceback.format_exc(),
        }
