from flask import request, redirect, url_for, flash, Blueprint
from flask_login import login_required
from datetime import datetime

from models.difunto_model import Difunto
from views import difunto_view

difunto_bp = Blueprint('difunto',__name__,url_prefix='/difuntos')

@difunto_bp.route("/")
@login_required
def index():
    difuntos = Difunto.get_all()
    return difunto_view.list(difuntos)

@difunto_bp.route("/create", methods=['POST'])
@login_required
def create():
    if request.method == 'POST':
        nombre = request.form['nombre']
        genero = request.form['genero']
        fecha_nacimiento = request.form['fecha_nacimiento']
        fecha_defuncion = request.form['fecha_defuncion']
        cedula_identidad = request.form['cedula_identidad']
        estado_civil = request.form['estado_civil']
        causa_muerte = request.form['causa_muerte']
        cliente_id = request.form['cliente_id']

        fecha_n = datetime.strptime(fecha_nacimiento,'%Y-%m-%d').date()
        fecha_d = datetime.strptime(fecha_defuncion,'%Y-%m-%d').date()

        difunto = Difunto(nombre=nombre, genero=genero, fecha_nacimiento=fecha_n, fecha_defuncion=fecha_d, cedula_identidad=cedula_identidad, estado_civil=estado_civil, causa_muerte=causa_muerte, cliente_id=cliente_id)
        difunto.save()
        flash("Difunto registrado correctamente", "success")
    return redirect(url_for("difunto.index"))

@difunto_bp.route("/edit/<int:id>", methods=['POST'])
@login_required
def edit(id):
    difunto = Difunto.get_by_id(id)
    if difunto:
        nombre = request.form['nombre']
        genero = request.form['genero']
        fecha_nacimiento_str = request.form['fecha_nacimiento']
        fecha_defuncion_str = request.form['fecha_defuncion']
        cedula_identidad = request.form['cedula_identidad']
        estado_civil = request.form['estado_civil']
        causa_muerte = request.form['causa_muerte']
        cliente_id = request.form['cliente_id']

        fecha_defuncion = datetime.strptime(fecha_defuncion_str, '%Y-%m-%d').date()
        fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, '%Y-%m-%d').date()    

        difunto.update(nombre=nombre, genero=genero, fecha_nacimiento=fecha_nacimiento, fecha_defuncion=fecha_defuncion, cedula_identidad=cedula_identidad, estado_civil=estado_civil, causa_muerte=causa_muerte, cliente_id=cliente_id)
        flash("Difunto actualizado", "success")
    else:
        flash("Difunto no encontrado", "danger")

    return redirect(url_for('difunto.index'))

@difunto_bp.route("/delete/<int:id>")
@login_required
def delete(id):
    difunto = Difunto.get_by_id(id)
    if difunto:
        difunto.delete()
        flash("Difunto eliminado", "success")
    else:
        flash("Difunto no encontrado", "danger")

    return redirect(url_for("difunto.index"))

