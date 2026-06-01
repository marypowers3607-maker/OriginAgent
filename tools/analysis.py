from tools.execute_labtalk import execute as execute_labtalk

def run_analysis(analysis):
    if not analysis:
        return None

    if isinstance(analysis, str):
        analysis_type = analysis.lower()
        params = {}
    else:
        analysis_type = str(analysis.get("type", "")).lower()
        params = analysis.get("params", {})

    # 这里不强行写死 Origin 所有分析功能。
    # 高频分析可以逐步封装；冷门分析直接用 labtalk 字段执行。

    if analysis_type in ["none", ""]:
        return None

    if analysis_type == "custom_labtalk":
        return execute_labtalk(params.get("script", ""))

    raise NotImplementedError(
        f"Analysis '{analysis_type}' is not wrapped yet. "
        f"Use task.labtalk or analysis.type='custom_labtalk' to run Origin commands directly."
    )
