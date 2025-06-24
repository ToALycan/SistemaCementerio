from flask import Flask, render_template
from flask_login import LoginManager, current_user
from database import db
from controllers import usuario_controller, log_controller, cliente_controller, difunto_controller, espacio_controller, servicio_controller, pago_controller, mantenimiento_controller, contrato_controller, dashboard_controller

from models.cliente_model import Cliente
from models.usuario_model import Usuario
from models.difunto_model import Difunto
from models.espacio_model import Espacio
from models.servicio_model import Servicio


app = Flask(__name__)
app.secret_key = 'clave_secreta_segura'

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cementerio.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

app.register_blueprint(usuario_controller.usuario_bp)
app.register_blueprint(log_controller.log_bp)   
app.register_blueprint(cliente_controller.cliente_bp)
app.register_blueprint(difunto_controller.difunto_bp)
app.register_blueprint(espacio_controller.espacio_bp)
app.register_blueprint(servicio_controller.servicio_bp)
app.register_blueprint(pago_controller.pago_bp)
app.register_blueprint(mantenimiento_controller.mantenimiento_bp)
app.register_blueprint(contrato_controller.contrato_bp)
app.register_blueprint(dashboard_controller.dashboard_bp)

@app.route('/')
def index():
    return render_template('inicio.html') 

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login.login'

@login_manager.user_loader
def load_user(user_id):
    return Usuario.get_by_id(user_id)

@app.context_processor
def inject_clientes():
    if current_user.is_authenticated:
        return dict(clientes=Cliente.query.all())
    return {}

@app.context_processor
def inject_difuntos():
    if current_user.is_authenticated:
        return dict(difuntos=Difunto.query.all())
    return {}

@app.context_processor
def inject_espacios():
    if current_user.is_authenticated:
        return dict(espacios=Espacio.query.all())
    return {}

@app.context_processor
def inject_servicios():
    if current_user.is_authenticated:
        return dict(servicios=Servicio.query.all())
    return {}
@app.context_processor
def inject_servicios():
    if current_user.is_authenticated:
        return dict(servicios=Servicio.query.all())
    return {}
    

@app.context_processor
def inject_common_variables():
    if current_user.is_authenticated:
        return {
            'ingresos_totales': db.session.query(db.func.sum(Servicio.costo))
                                .filter(Servicio.estado == 'Pagado').scalar() or 0,
            # otras variables comunes
        }
    return {}

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)