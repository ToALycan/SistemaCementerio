from flask import request, redirect, url_for, flash, Blueprint
from flask_login import login_required
from datetime import datetime

from models.mantenimiento_model import Mantenimiento
from views import mantenimiento_view

mantenimiento_bp = Blueprint('mantenimiento',__name__,url_prefix='/mantenimientos')

@mantenimiento_bp.route("/")
@login_required
def index():
    mantenimientos = Mantenimiento.get_all()
    return mantenimiento_view.list(mantenimientos)

@mantenimiento_bp.route("/create", methods=['POST'])
@login_required
def create():
    try:
        espacio_id = request.form['espacio_id']
        descripcion = request.form['descripcion']
        fecha_programada_str = request.form['fecha_programada']
        costo = request.form['costo']
        estado = 'Programado'

        fecha_programada = datetime.strptime(fecha_programada_str, '%Y-%m-%d').date()

        # Crear mantenimiento con fecha_realizado=None por defecto
        mantenimiento = Mantenimiento(
            espacio_id=espacio_id,
            descripcion=descripcion,
            fecha_programada=fecha_programada,
            costo=costo,
            estado=estado
        )
        
        mantenimiento.save()
        flash("Mantenimiento creado con éxito", "success")
        
    except ValueError as e:
        flash("Error en formato de fecha: use el formato AAAA-MM-DD", "danger")
    except Exception as e:
        flash(f"Error al crear mantenimiento: {str(e)}", "danger")
        
    return redirect(url_for("mantenimiento.index"))

@mantenimiento_bp.route("/edit/<int:id>", methods=['POST'])
@login_required
def edit(id):
    mantenimiento = Mantenimiento.get_by_id(id)
    if mantenimiento:
        try:
            # Obtener datos del formulario
            data = {
                'espacio_id': request.form['espacio_id'],
                'descripcion': request.form['descripcion'],
                'fecha_programada': datetime.strptime(request.form['fecha_programada'], '%Y-%m-%d').date(),
                'costo': float(request.form['costo']),
                'estado': request.form['estado']
            }

            # Manejar fecha_realizado según estado
            if data['estado'] in ['Realizado', 'Cancelado']:
                if not mantenimiento.fecha_realizado:  # Solo actualizar si no tenía fecha
                    data['fecha_realizado'] = datetime.now().date()
                    
            elif data['estado'] == 'Programado':
                data['fecha_realizado'] = None

            mantenimiento.update(**data)
            flash("Mantenimiento actualizado correctamente", "success")
            
        except ValueError as e:
            flash("Error en formato de fecha o número: verifique los datos", "danger")
        except Exception as e:
            flash(f"Error al actualizar: {str(e)}", "danger")
    else:
        flash("Mantenimiento no encontrado", "danger")

    return redirect(url_for('mantenimiento.index'))

@mantenimiento_bp.route("/delete/<int:id>")
@login_required
def delete(id):
    mantenimiento = Mantenimiento.get_by_id(id)
    if mantenimiento:
        mantenimiento.delete()
        flash("mantenimiento eliminado", "success")
    else:
        flash("mantenimiento no encontrado", "danger")

    return redirect(url_for("mantenimiento.index"))

from flask import send_file
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from io import BytesIO

@mantenimiento_bp.route("/aviso/<int:id>")
@login_required
def generar_aviso(id):
    mantenimiento = Mantenimiento.get_by_id(id)
    if not mantenimiento:
        flash("Mantenimiento no encontrado", "danger")
        return redirect(url_for("mantenimiento.index"))

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # --- Estilo: encabezado color azul
    c.setFillColor(colors.HexColor("#003366"))
    c.rect(0, height - 100, width, 100, stroke=0, fill=1)

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(width / 2, height - 60, "AVISO DE MANTENIMIENTO")

    # --- Contenedor principal
    c.setFillColor(colors.white)
    c.setStrokeColor(colors.HexColor("#003366"))
    c.setLineWidth(2)
    c.roundRect(40, height - 480, width - 80, 350, 10, stroke=1, fill=0)

    c.drawImage("static/img/logo.jpg", 40, height - 80, width=80, height=70)

    # Datos internos
    y = height - 150
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 12)

    def draw_field(label, value):
        nonlocal y
        c.setFont("Helvetica-Bold", 12)
        c.drawString(60, y, f"{label}:")
        c.setFont("Helvetica", 12)
        c.drawString(220, y, str(value))
        y -= 30

    espacio_text = "Sin asignar"
    if mantenimiento.espacio:
        espacio_text = f"{mantenimiento.espacio.tipo} - Sector {mantenimiento.espacio.sector}, N° {mantenimiento.espacio.numero}"

    draw_field("ID Mantenimiento", mantenimiento.id)
    draw_field("Espacio", espacio_text)
    draw_field("Descripción", mantenimiento.descripcion)
    draw_field("Fecha Programada", mantenimiento.fecha_programada.strftime("%d/%m/%Y"))
    draw_field("Costo", f"Bs. {mantenimiento.costo:.2f}")
    draw_field("Estado", mantenimiento.estado)
    if mantenimiento.fecha_realizado:
        draw_field("Fecha Realizado", mantenimiento.fecha_realizado.strftime("%d/%m/%Y"))
    else:
        draw_field("Fecha Realizado", "Pendiente")

    # Firma (opcional)
    c.setFont("Helvetica-Oblique", 12)
    c.drawString(60, y - 20, "Firma Responsable:")
    c.line(200, y - 25, 500, y - 25)

    # Pie elegante
    c.setFillColor(colors.HexColor("#003366"))
    c.rect(0, 0, width, 50, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont("Helvetica", 10)
    c.drawCentredString(width / 2, 20, "Cementerio Municipal | contacto@cementerio.bo")

    c.showPage()
    c.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name=f"aviso_mantenimiento_{mantenimiento.id}.pdf", mimetype='application/pdf')
