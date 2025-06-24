from flask import render_template

def list(contratos):
    return render_template('contratos/index.html', contratos=contratos)