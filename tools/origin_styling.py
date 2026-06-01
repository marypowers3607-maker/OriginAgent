from tools.execute_labtalk import execute as execute_labtalk
from tools.execute_origin_python import execute as execute_origin_python


def apply_origin_styling(style_commands=None, graph=None, context=None):
    commands = _normalize_commands(style_commands)
    results = []

    if not commands:
        return {
            "status": "skipped",
            "message": "No style commands provided",
            "results": results,
        }

    ctx = {} if context is None else dict(context)
    if graph is not None:
        ctx["graph"] = graph

    for command in commands:
        command_type = str(command.get("type", "origin_python")).lower()
        value = command.get("code") or command.get("script") or ""

        if command_type in ["origin_python", "python", "op"]:
            result = execute_origin_python(value, ctx)
        elif command_type in ["labtalk", "lt"]:
            result = execute_labtalk(value)
        else:
            result = {
                "status": "error",
                "error": f"Unsupported style command type: {command_type}",
            }

        results.append({
            "type": command_type,
            "result": result,
        })

    status = "error" if any(item["result"].get("status") == "error" for item in results if isinstance(item.get("result"), dict)) else "success"
    return {
        "status": status,
        "results": results,
    }


def _normalize_commands(style_commands):
    if not style_commands:
        return []
    if isinstance(style_commands, str):
        return [{"type": "origin_python", "code": style_commands}]
    if isinstance(style_commands, dict):
        return [style_commands]
    return list(style_commands)
