from flask import render_template

def list(clientes):
    return render_template('clientes/index.html', clientes=clientes)