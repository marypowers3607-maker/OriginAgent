import originpro as op

def plot_line(wks, x_col, y_col):
    gp = op.new_graph()
    gl = gp[0]
    gl.add_plot(wks, colx=x_col, coly=y_col)
    gl.rescale()
    return gp

def plot_scatter(wks, x_col, y_col):
    gp = op.new_graph()
    gl = gp[0]
    gl.add_plot(wks, colx=x_col, coly=y_col, type="s")
    gl.rescale()
    return gp

def plot_multi_line(wks, x_col, y_cols):
    gp = op.new_graph()
    gl = gp[0]

    for y_col in y_cols:
        gl.add_plot(wks, colx=x_col, coly=y_col)

    gl.rescale()
    return gp

def plot_multi_scatter(wks, x_col, y_cols):
    gp = op.new_graph()
    gl = gp[0]

    for y_col in y_cols:
        gl.add_plot(wks, colx=x_col, coly=y_col, type="s")

    gl.rescale()
    return gp
