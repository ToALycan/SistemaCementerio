from flask import render_template
def list(difuntos):
    return render_template('difuntos/index.html', difuntos=difuntos)