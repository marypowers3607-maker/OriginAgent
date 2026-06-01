def resolve_template(template, plot_type=None):
    if template in [None, "", "none", "null"]:
        return {
            "status": "skipped",
            "template": None,
            "plot_type": plot_type,
        }

    template_name = str(template)
    known = {
        "line": "line",
        "scatter": "scatter",
        "column": "column",
        "bar": "column",
    }

    return {
        "status": "resolved",
        "template": known.get(template_name.lower(), template_name),
        "plot_type": plot_type,
    }


def template_for_plot(template, plot_type=None):
    resolved = resolve_template(template, plot_type)
    return resolved["template"]
