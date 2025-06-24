from flask import render_template

def list(usuarios):
    return render_template('usuarios/index.html', usuarios=usuarios)

def login():
    return render_template('login.html')

def register():
    return render_template('register.html')

def dashboard():
    return render_template('dashboard.html')
    
