from flask import render_template

def list(espacios):
    return render_template('espacios/index.html', espacios=espacios)