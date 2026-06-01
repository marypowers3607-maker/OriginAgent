import originpro as op

def _new_graph():
    gp = op.new_graph()
    gl = gp[0]
    return gp, gl

def plot_line(wks, x_col, y_cols):
    gp, gl = _new_graph()
    for y in y_cols:
        gl.add_plot(wks, colx=x_col, coly=y)
    gl.rescale()
    return gp

def plot_scatter(wks, x_col, y_cols):
    gp, gl = _new_graph()
    for y in y_cols:
        gl.add_plot(wks, colx=x_col, coly=y, type="s")
    gl.rescale()
    return gp

def plot_column(wks, x_col, y_cols):
    gp, gl = _new_graph()
    for y in y_cols:
        gl.add_plot(wks, colx=x_col, coly=y, type="column")
    gl.rescale()
    return gp

def plot_with_template(wks, template_name, x_col, y_cols):
    gp = op.new_graph(template=template_name)
    gl = gp[0]
    for y in y_cols:
        gl.add_plot(wks, colx=x_col, coly=y)
    gl.rescale()
    return gp
