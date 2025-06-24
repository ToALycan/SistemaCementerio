from flask import request,render_template, redirect, url_for, flash, Blueprint
from flask_login import login_user, logout_user, login_required

from models.usuario_model import Usuario
from views import usuario_view

log_bp = Blueprint('login', __name__,__name__,url_prefix="/login")


@log_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Usuario.get_by_username(username)

        if user and user.verify_password(password):
            login_user(user)
            flash('Inicio de Sesión exitoso', 'success')

            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard.index'))  # <--- redirige a 'next' o al index

        else:
            flash('Credenciales inválidas', 'danger')

    return usuario_view.login()


@log_bp.route("/register", methods=['GET','POST'])
def register():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        username = request.form.get('username')
        password = request.form.get('password')
        rol = request.form.get('rol')

        usuario = Usuario(nombre=nombre, username=username, password=password, rol=rol)
        usuario.save()

        flash("Usuario Registrado Correctamente", "success")
    return usuario_view.register()

@log_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@log_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión', 'info')
    return redirect(url_for('index'))
