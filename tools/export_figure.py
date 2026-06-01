from pathlib import Path

def export_graph(graph_page, export_config):
    outputs = []

    if isinstance(export_config, str):
        paths = [export_config]
    else:
        paths = export_config.get("paths")
        if paths is None:
            path = export_config.get("path")
            paths = [path] if path else []

    for p in paths:
        out = Path(p)
        out.parent.mkdir(parents=True, exist_ok=True)
        graph_page.save_fig(str(out))
        outputs.append(str(out))

    return outputs
