from flask import request, redirect, url_for, flash, Blueprint
from flask_login import login_required
from flask import send_file
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from models.pago_model import Pago
from models.servicio_model import Servicio
from views import pago_view
from reportlab.lib.units import inch
from reportlab.lib import colors

pago_bp = Blueprint('pago',__name__,url_prefix='/pagos')

@pago_bp.route("/")
@login_required
def index():
    pagos = Pago.get_all()
    return pago_view.list(pagos)

@pago_bp.route("/create", methods=['POST'])
@login_required
def create():
    cliente_id = request.form['cliente_id']
    servicio_id = request.form['servicio_id']
    monto = request.form['monto']
    metodo_pago = request.form['metodo_pago']
    referencia = request.form['referencia']
    
    pago = Pago(cliente_id=cliente_id, servicio_id=servicio_id, monto=monto, metodo_pago=metodo_pago, referencia=referencia)
    pago.save()

    if servicio_id:
        servicio = Servicio.get_by_id(servicio_id)
        if servicio:
            servicio.estado = 'Pagado'
            servicio.save()

    flash("pago creado con exito", "success")
    return redirect(url_for("pago.index"))

@pago_bp.route("/edit/<int:id>", methods=['POST'])
@login_required
def edit(id):
    pago = Pago.get_by_id(id)
    if pago:
        cliente_id = request.form['cliente_id']
        servicio_id = request.form['servicio_id']
        monto = request.form['monto']
        metodo_pago = request.form['metodo_pago']
        referencia = request.form['referencia']

        pago.update(cliente_id=cliente_id, servicio_id=servicio_id, monto=monto, metodo_pago=metodo_pago, referencia=referencia)
        flash("pago actualizado", "success")
    else:
        flash("pago no encontrado", "danger")

    return redirect(url_for('pago.index'))

@pago_bp.route("/delete/<int:id>")
@login_required
def delete(id):
    pago = Pago.get_by_id(id)
    if pago:
        pago.delete()
        flash("pago eliminado", "success")
    else:
        flash("pago no encontrado", "danger")

    return redirect(url_for("pago.index"))


@pago_bp.route("/recibo/<int:id>")
@login_required
def generar_recibo(id):
    pago = Pago.get_by_id(id)
    if not pago:
        flash("Pago no encontrado", "danger")
        return redirect(url_for("pago.index"))

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # --- Estilo: Encabezado de color
    c.setFillColor(colors.HexColor("#003366"))
    c.rect(0, height - 100, width, 100, stroke=0, fill=1)

    # Logo (opcional)
    c.drawImage("static/img/logo.jpg", 40, height - 80, width=80, height=70)

    # Título centrado
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, height - 60, "RECIBO DE PAGO")

    # --- Contenedor principal
    c.setFillColor(colors.white)
    c.setStrokeColor(colors.HexColor("#003366"))
    c.setLineWidth(2)
    c.roundRect(40, height - 480, width - 80, 350, 10, stroke=1, fill=0)

    # Datos internos
    y = height - 180
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 12)

    def draw_field(label, value):
        nonlocal y
        c.setFont("Helvetica-Bold", 12)
        c.drawString(60, y, f"{label}:")
        c.setFont("Helvetica", 12)
        c.drawString(200, y, str(value))
        y -= 25

    draw_field("N° de Recibo", pago.id)
    draw_field("Cliente", pago.cliente.nombre)
    draw_field("Servicio", pago.servicio.tipo)
    draw_field("Monto Pagado", f"Bs. {pago.monto:.2f}")
    draw_field("Método de Pago", pago.metodo_pago)
    draw_field("Referencia", pago.referencia or "N/A")
    draw_field("Fecha", pago.fecha.strftime("%d/%m/%Y"))

    # Línea de firma
    c.setFont("Helvetica-Oblique", 12)
    c.drawString(60, y - 20, "Firma del Responsable:")
    c.line(200, y - 25, 500, y - 25)

    # --- Pie elegante
    c.setFillColor(colors.HexColor("#003366"))
    c.rect(0, 0, width, 50, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont("Helvetica", 10)
    c.drawCentredString(width / 2, 20, "Gracias por su pago. Cementerio Municipal | contacto@cementerio.bo")

    c.showPage()
    c.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name=f"recibo_pago_{pago.id}.pdf", mimetype='application/pdf')