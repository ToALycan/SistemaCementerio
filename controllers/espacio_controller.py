from flask import request, redirect, url_for, flash, Blueprint
from flask_login import login_required
from datetime import datetime

from models.espacio_model import Espacio
from views import espacio_view

espacio_bp = Blueprint('espacio',__name__,url_prefix='/espacios')

@espacio_bp.route("/")
@login_required
def index():
    espacios = Espacio.get_all()
    return espacio_view.list(espacios)

@espacio_bp.route("/create", methods=['POST'])
@login_required
def create():
    numero = request.form['numero']
    tipo = request.form['tipo']
    descripcion = request.form['descripcion']
    sector = request.form['sector']
    pabellon = request.form['pabellon']
    fila = request.form['fila']
    estado = request.form['estado']
    fecha_str = request.form['fecha_ocupacion']
    difunto_id = request.form['difunto_id']

    fecha_ocupacion = datetime.strptime(fecha_str, '%Y-%m-%d').date()

    espacio = Espacio(numero=numero, tipo=tipo, descripcion=descripcion, sector=sector, pabellon=pabellon, fila=fila, estado=estado, fecha_ocupacion=fecha_ocupacion, difunto_id=difunto_id)
    espacio.save()

    flash("Espacio creado con exito", "success")
    return redirect(url_for("espacio.index"))

@espacio_bp.route("/edit/<int:id>", methods=['POST'])
@login_required
def edit(id):
    espacio = Espacio.get_by_id(id)
    if espacio:
        numero = request.form['numero']
        tipo = request.form['tipo']
        descripcion = request.form['descripcion']
        sector = request.form['sector']
        pabellon = request.form['pabellon']
        fila = request.form['fila']
        estado = request.form['estado']
        fecha_str = request.form['fecha_ocupacion']
        difunto_id = request.form['difunto_id']

        fecha_ocupacion = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        
        espacio.update(numero=numero, tipo=tipo, descripcion=descripcion, sector=sector, pabellon=pabellon, fila=fila, estado=estado, fecha_ocupacion=fecha_ocupacion, difunto_id=difunto_id)
        flash("Espacio actualizado", "success")
    else:
        flash("Espacio no encontrado", "danger")

    return redirect(url_for('espacio.index'))

@espacio_bp.route("/delete/<int:id>")
@login_required
def delete(id):
    espacio = Espacio.get_by_id(id)
    if espacio:
        espacio.delete()
        flash("Espacio eliminado", "success")
    else:
        flash("Espacio no encontrado", "danger")

    return redirect(url_for("espacio.index"))

