from flask import request, redirect, url_for, flash, Blueprint
from flask_login import login_required
from datetime import datetime

from models.contrato_model import Contrato
from views import contrato_view

contrato_bp = Blueprint('contrato',__name__,url_prefix='/contratos')

@contrato_bp.route("/")
@login_required
def index():
    contratos = Contrato.get_all()
    return contrato_view.list(contratos)

@contrato_bp.route("/create", methods=['POST'])
@login_required
def create():
    cliente_id = request.form['cliente_id']
    espacio_id = request.form['espacio_id']
    fecha_inicio_str = request.form['fecha_inicio']

    tipo = request.form['tipo']
    costo = request.form['costo']
    estado = 'Activo'
    
    fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
    if tipo.lower() == 'perpetuo':
        fecha_fin = "Perpetuo"  # Guardamos como string
    else:
        # Calculamos 5 años después para contratos temporales
        fecha_fin = fecha_inicio.replace(year=fecha_inicio.year + 5)
        # Convertimos a string en formato DD-MM-YYYY
        fecha_fin = fecha_fin.strftime('%d-%m-%Y')

    contrato = Contrato(cliente_id=cliente_id, espacio_id=espacio_id, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, tipo=tipo, costo=costo, estado=estado)
    contrato.save()

    flash("contrato creado con exito", "success")
    return redirect(url_for("contrato.index"))

@contrato_bp.route("/edit/<int:id>", methods=['POST'])
@login_required
def edit(id):
    contrato = Contrato.get_by_id(id)
    if contrato:
        cliente_id = request.form['cliente_id']
        espacio_id = request.form['espacio_id']
        fecha_inicio_str = request.form['fecha_inicio']
        fecha_fin_str = request.form['fecha_fin']
        tipo = request.form['tipo']
        costo = request.form['costo']
        estado = request.form['estado']

        fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
        fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()

        contrato.update(cliente_id=cliente_id, espacio_id=espacio_id, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, tipo=tipo, costo=costo, estado=estado)
        flash("contrato actualizado", "success")
    else:
        flash("contrato no encontrado", "danger")

    return redirect(url_for('contrato.index'))

from flask import send_file
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch


@contrato_bp.route("/delete/<int:id>")
@login_required
def delete(id):
    contrato = Contrato.get_by_id(id)
    if contrato:
        contrato.delete()
        flash("contrato eliminado", "success")
    else:
        flash("contrato no encontrado", "danger")

    return redirect(url_for("contrato.index"))

@contrato_bp.route("/pdf/<int:id>")
@login_required
def generar_contrato_pdf(id):
    contrato = Contrato.get_by_id(id)
    if not contrato:
        flash("Contrato no encontrado", "danger")
        return redirect(url_for("contrato.index"))

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # ─── Encabezado con color ─────────────────────────────────────────
    c.setFillColor(colors.HexColor("#003366"))
    c.rect(0, height - 80, width, 80, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width/2, height - 50, "CONTRATO DE SERVICIOS")

    # ─── Cuerpo del contrato ──────────────────────────────────────────
    text = c.beginText(50, height - 120)
    text.setFont("Helvetica", 11)
    text.setLeading(16)
    text.setFillColor(colors.black)

    # Título de la cláusula
    text.setFont("Helvetica-Bold", 12)
    text.textLine(f"Nº de Contrato: {contrato.id}")
    text.textLine("")

    # Párrafo introductorio
    text.setFont("Helvetica", 11)
    intro = (
    f"En la ciudad, a fecha {contrato.fecha_inicio.strftime('%d/%m/%Y')},\n"
    f"comparecen: el Cliente (ID {contrato.cliente_id}) y el Cementerio Municipal,\n"
    f"para celebrar el presente contrato de tipo '{contrato.tipo}'."
)
    text.textLines(intro)
    text.textLine("")

    # Detalles esenciales
    campos = [
        ("Cliente", contrato.cliente.nombre if contrato.cliente else "N/A"),
        ("Espacio", f"Sector {contrato.espacio.sector}, Nº {contrato.espacio.numero}" if contrato.espacio else "N/A"),
        ("Fecha Inicio", contrato.fecha_inicio.strftime('%d/%m/%Y')),
        ("Fecha Fin", "Perpetuo" if contrato.tipo.lower() == "perpetuo" else contrato.fecha_fin.strftime('%d/%m/%Y') if contrato.fecha_fin else "No especificada"),
        ("Costo", f"Bs. {float(contrato.costo):.2f}"),
        ("Estado", contrato.estado),
    ]
    for label, val in campos:
        text.setFont("Helvetica-Bold", 11)
        text.textOut(f"{label}: ")
        text.setFont("Helvetica", 11)
        text.textLine(str(val))
    text.textLine("")
    
    # Cláusulas estándar (ejemplo)
    clausulas = [
        "1. Objeto del contrato: Prestación del servicio funerario.",
        "2. Obligaciones del Cliente: Abonar el coste en los términos establecidos.",
        "3. Duración y renovación: El contrato se renovará a partir de la fecha de vencimiento del servicio.",
        "4. Jurisdicción: Se aplicará la ley de contrataciones municipales."
    ]
    for ctext in clausulas:
        text.textLine(ctext)
        text.textLine("")

    c.drawText(text)

    c.drawImage("static/img/logo.jpg", 40, height - 80, width=80, height=70)

    # ─── Firma ─────────────────────────────────────────────────────────
    y_firma = 120
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y_firma, "Firma del Cliente:")
    c.line(180, y_firma, 400, y_firma)
    c.drawString(50, y_firma - 30, "Firma del Representante Municipal:")
    c.line(260, y_firma - 30, 550, y_firma - 30)

    # ─── Pie de página ────────────────────────────────────────────────
    c.setFillColor(colors.HexColor("#003366"))
    c.rect(0, 0, width, 40, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Oblique", 9)
    c.drawCentredString(width/2, 15, "Cementerio Municipal • Contrato oficial • www.cementerio.bo")

    c.showPage()
    c.save()
    buffer.seek(0)

    return send_file(buffer,
                     as_attachment=True,
                     download_name=f"contrato_{contrato.id}.pdf",
                     mimetype="application/pdf")
