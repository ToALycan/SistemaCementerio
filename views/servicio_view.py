from flask import render_template

def list(servicios):
    return render_template('servicios/index.html', servicios=servicios)