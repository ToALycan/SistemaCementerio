from flask import request, redirect, url_for, flash, Blueprint
from flask_login import login_required
from datetime import datetime

from models.servicio_model import Servicio
from views import servicio_view

servicio_bp = Blueprint('servicio',__name__,url_prefix='/servicios')

@servicio_bp.route("/")
@login_required
def index():
    servicios = Servicio.get_all()
    return servicio_view.list(servicios)

@servicio_bp.route("/create", methods=['POST'])
@login_required
def create():
    tipo = request.form['tipo']
    descripcion = request.form['descripcion']
    fecha_str = request.form['fecha']
    hora_str = request.form['hora']
    cliente_id = request.form['cliente_id']
    difunto_id = request.form['difunto_id']
    espacio_id = request.form['espacio_id']
    costo = request.form['costo']
    estado = request.form['estado']

    fecha = datetime.strptime(fecha_str,'%Y-%m-%d').date()
    hora = datetime.strptime(hora_str, '%H:%M').time()


    servicio = Servicio(tipo=tipo, descripcion=descripcion, fecha=fecha, hora=hora, cliente_id=cliente_id, difunto_id=difunto_id, espacio_id=espacio_id, costo=costo, estado=estado)
    servicio.save()

    flash("servicio creado con exito", "success")
    return redirect(url_for("servicio.index"))

@servicio_bp.route("/edit/<int:id>", methods=['POST'])
@login_required
def edit(id):
    servicio = Servicio.get_by_id(id)
    if servicio:
        tipo = request.form['tipo']
        descripcion = request.form['descripcion']
        fecha_str = request.form['fecha']
        hora_str = request.form['hora']
        cliente_id = request.form['cliente_id']
        difunto_id = request.form['difunto_id']
        espacio_id = request.form['espacio_id']
        costo = request.form['costo']
        estado = request.form['estado']

        fecha = datetime.strptime(fecha_str,'%Y-%m-%d').date()
        hora = datetime.strptime(hora_str, '%H:%M:%S').time()


        servicio.update(tipo=tipo, descripcion=descripcion, fecha=fecha, hora=hora, cliente_id=cliente_id, difunto_id=difunto_id, espacio_id=espacio_id, costo=costo, estado=estado)
        flash("servicio actualizado", "success")
    else:
        flash("servicio no encontrado", "danger")

    return redirect(url_for('servicio.index'))

@servicio_bp.route("/delete/<int:id>")
@login_required
def delete(id):
    servicio = Servicio.get_by_id(id)
    if servicio:
        servicio.delete()
        flash("servicio eliminado", "success")
    else:
        flash("servicio no encontrado", "danger")

    return redirect(url_for("servicio.index"))

from flask import send_file
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

@servicio_bp.route("/recibo/<int:id>")
@login_required
def generar_servicio_pdf(id):
    servicio = Servicio.get_by_id(id)
    if not servicio:
        flash("Servicio no encontrado", "danger")
        return redirect(url_for("servicio.index"))

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Encabezado
    c.setFillColor(colors.HexColor("#003366"))
    c.rect(0, height - 100, width, 100, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, height - 60, "DETALLE DEL SERVICIO")
    
    c.drawImage("static/img/logo.jpg", 40, height - 80, width=80, height=70)


    # Recuadro de datos
    c.setStrokeColor(colors.HexColor("#003366"))
    c.setLineWidth(2)
    c.roundRect(40, height - 500, width - 80, 370, 10, stroke=1, fill=0)

    y = height - 180
    line_height = 25

    def draw_field(label, value):
        nonlocal y
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(colors.HexColor("#003366"))
        c.drawString(60, y, f"{label}:")
        c.setFont("Helvetica", 12)
        c.setFillColor(colors.black)
        c.drawString(200, y, str(value))
        y -= line_height

    draw_field("ID del Servicio", servicio.id)
    draw_field("Tipo", servicio.tipo)
    draw_field("Descripción", servicio.descripcion)
    draw_field("Cliente", servicio.cliente.nombre if servicio.cliente else "No asignado")
    draw_field("Difunto", servicio.difunto.nombre if servicio.difunto else "No asignado")
    draw_field("Fecha", servicio.fecha.strftime("%d/%m/%Y"))
    draw_field("Hora", servicio.hora.strftime("%H:%M"))
    draw_field("Ubicación", f"Sector {servicio.espacio.sector}, N° {servicio.espacio.numero}" if servicio.espacio else "No asignado")
    draw_field("Costo", f"Bs. {servicio.costo:.2f}")
    draw_field("Estado", servicio.estado)

    # Firma
    y -= 30
    c.setFont("Helvetica-Oblique", 12)
    c.drawString(60, y, "Firma del Responsable:")
    c.line(200, y - 5, 500, y - 5)

    # Pie de página
    c.setFillColor(colors.HexColor("#003366"))
    c.rect(0, 0, width, 50, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont("Helvetica", 10)
    c.drawCentredString(width / 2, 20, "Cementerio Municipal - Sistema de Gestión de Servicios")

    c.showPage()
    c.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name=f"servicio_{servicio.id}.pdf", mimetype='application/pdf')
