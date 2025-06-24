from flask import request, redirect, url_for, flash, Blueprint
from flask_login import login_required

from models.cliente_model import Cliente
from views import cliente_view

cliente_bp = Blueprint('cliente',__name__,url_prefix='/clientes')

@cliente_bp.route("/")
@login_required
def index():
    clientes = Cliente.get_all()
    return cliente_view.list(clientes)

@cliente_bp.route("/create", methods=['POST'])
@login_required
def create():
    nombre = request.form['nombre']
    telefono = request.form['telefono']
    email = request.form['email']
    direccion = request.form['direccion']

    cliente = Cliente(nombre=nombre, telefono=telefono, email=email, direccion=direccion)
    cliente.save()

    flash("Cliente creado con exito", "success")
    return redirect(url_for("cliente.index"))

@cliente_bp.route("/edit/<int:id>", methods=['POST'])
@login_required
def edit(id):
    cliente = Cliente.get_by_id(id)
    if cliente:
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        email = request.form['email']
        direccion = request.form['direccion']

        cliente.update(nombre=nombre, telefono=telefono, email=email, direccion=direccion)
        flash("Cliente actualizado", "success")
    else:
        flash("Cliente no encontrado", "danger")

    return redirect(url_for('cliente.index'))

@cliente_bp.route("/delete/<int:id>")
@login_required
def delete(id):
    cliente = Cliente.get_by_id(id)
    if cliente:
        cliente.delete()
        flash("Cliente eliminado", "success")
    else:
        flash("Cliente no encontrado", "danger")

    return redirect(url_for("cliente.index"))

