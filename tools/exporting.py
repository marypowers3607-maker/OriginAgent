from pathlib import Path

def export_graph(graph_page, export_config):
    if graph_page is None:
        return []

    if not export_config:
        return []

    if isinstance(export_config, str):
        paths = [export_config]
    else:
        paths = export_config.get("paths")
        if paths is None:
            single = export_config.get("path")
            paths = [single] if single else []

    outputs = []
    for path in paths:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        graph_page.save_fig(str(out))
        outputs.append(str(out))

    return outputs
