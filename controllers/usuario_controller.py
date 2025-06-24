from flask import request, redirect, url_for, flash, Blueprint
from flask_login import login_required, current_user

from models.usuario_model import Usuario
from views import usuario_view

usuario_bp = Blueprint('usuario',__name__,url_prefix="/usuarios")

@usuario_bp.route("/")
@login_required
def index():
    usuarios = Usuario.get_all()
    return usuario_view.list(usuarios)

@usuario_bp.route("/create", methods=['POST'])
@login_required
def create():
    nombre = request.form['nombre']
    username = request.form['username']
    password = request.form['password']
    rol = request.form['rol']
    
    usuario = Usuario(nombre=nombre, username=username, password=password, rol=rol)
    usuario.save()

    flash("Usuario creado con exito", "success")
    return redirect(url_for("usuario.index"))

@usuario_bp.route("/edit/<int:id>", methods=['POST'])
@login_required
def edit(id):
    usuario = Usuario.get_by_id(id)
    if usuario:
        nombre = request.form['nombre']
        username = request.form['username']
        rol = request.form['rol']

        usuario.update(nombre=nombre, username=username, rol=rol)
        flash("Usuario actualizado", "success")
    else:
        flash("Usuario no encontrado", "danger")

    return redirect(url_for('usuario.index'))

@usuario_bp.route("/delete/<int:id>")
@login_required
def delete(id):
    usuario = Usuario.get_by_id(id)
    if usuario:
        usuario.delete()
        flash("Usuario eliminado", "success")
    else:
        flash("Usuario no encontrado", "danger")

    return redirect(url_for("usuario.index"))

@usuario_bp.route("/reset_password/<int:id>", methods=['POST'])
def reset_password(id):
    usuario = Usuario.get_by_id(id)
    if usuario:
        new_password = usuario.username + "123"
        usuario.reset_password(new_password)
        flash(f"Contraseña restablecida a {new_password}", "warning")
    else:
        flash("Usuario no encontrado", "danger")
    return redirect(url_for("usuario.index"))

@usuario_bp.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    actual_password = request.form.get("actual_password")
    new_password = request.form.get("nuevo_password")
    confirmar_password = request.form.get("confirmar_password")

    if not actual_password or not new_password or not confirmar_password:
        flash("Debe completar todos los campos", "danger")
    elif new_password != confirmar_password:
         flash("Las contraseñas no coinciden", "danger")
    else:
         if current_user.change_password(actual_password, new_password):
             flash("Contraseña actualizada correctamente", "success")
         else:
             flash("La contraseña actual es incorrecta", "danger" )
    return redirect(url_for("usuario.index"))

