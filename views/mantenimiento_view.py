from flask import render_template

def list(mantenimientos):
    return render_template('mantenimientos/index.html', mantenimientos=mantenimientos)