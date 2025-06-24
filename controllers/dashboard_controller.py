from flask import Blueprint, render_template
from flask_login import login_required
from datetime import datetime, timedelta
from database import db
from models.cliente_model import Cliente
from models.difunto_model import Difunto
from models.espacio_model import Espacio
from models.servicio_model import Servicio
from models.contrato_model import Contrato
from models.mantenimiento_model import Mantenimiento

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard_bp.route("/")
@login_required
def index():
    # Estadísticas principales
    total_clientes = Cliente.query.count()
    total_difuntos = Difunto.query.count()
    total_espacios = Espacio.query.count()
    
    # Calcular ingresos totales (suma de servicios)
    ingresos_totales = db.session.query(db.func.sum(Servicio.costo))\
        .filter(Servicio.estado == 'Pagado').scalar() or 0
    
    # Obtener últimos 5 servicios - CONSULTA CORREGIDA
    servicios_recientes = db.session.query(
        Servicio,
        Cliente.nombre.label('cliente_nombre'),
        Difunto.nombre.label('difunto_nombre')
    ).select_from(Servicio)\
     .join(Cliente, Servicio.cliente_id == Cliente.id)\
     .join(Difunto, Servicio.difunto_id == Difunto.id)\
     .order_by(Servicio.fecha.desc())\
     .limit(5)\
     .all()
    
    # Mantenimientos pendientes
    mantenimientos_pendientes = Mantenimiento.query\
        .filter(Mantenimiento.estado == 'Programado')\
        .order_by(Mantenimiento.fecha_programada.asc())\
        .limit(5)\
        .all()
    
    # Contratos por vencer - CONSULTA CORREGIDA
    contratos_por_vencer = db.session.query(
        Contrato,
        Cliente.nombre.label('cliente_nombre')
    ).select_from(Contrato)\
     .join(Cliente, Contrato.cliente_id == Cliente.id)\
     .filter(Contrato.fecha_fin >= datetime.now())\
     .filter(Contrato.fecha_fin <= datetime.now() + timedelta(days=30))\
     .order_by(Contrato.fecha_fin.asc())\
     .limit(5)\
     .all()
    
    for contrato, cliente_nombre in contratos_por_vencer:
        if isinstance(contrato.fecha_fin, str):
            contrato.fecha_fin = datetime.strptime(contrato.fecha_fin, '%Y-%m-%d') 

    # Estadísticas de espacios
    espacios_disponibles = Espacio.query.filter_by(estado='Disponible').count()
    espacios_ocupados = Espacio.query.filter_by(estado='Ocupado').count()
    espacios_mantenimiento = Espacio.query.filter_by(estado='Mantenimiento').count()
    
    return render_template(
        'dash/index.html',
        total_clientes=total_clientes,
        total_difuntos=total_difuntos,
        total_espacios=total_espacios,
        ingresos_totales=ingresos_totales,
        servicios_recientes=servicios_recientes,
        mantenimientos_pendientes=mantenimientos_pendientes,
        contratos_por_vencer=contratos_por_vencer,
        espacios_disponibles=espacios_disponibles,
        espacios_ocupados=espacios_ocupados,
        espacios_mantenimiento=espacios_mantenimiento
    )