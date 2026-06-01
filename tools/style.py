import originpro as op

def apply_style(style: str = "default"):
    style = (style or "default").lower()

    if style in ["science", "sci", "nature", "paper"]:
        op.lt_exec("page -B 1;")
        op.lt_exec("legend -r;")
        op.lt_exec("layer -a;")
        return "science"

    return style
