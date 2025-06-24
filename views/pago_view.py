from flask import render_template

def list(pagos):
    return render_template('pagos/index.html', pagos=pagos)