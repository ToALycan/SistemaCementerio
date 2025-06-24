from datetime import datetime
from database import db

class Cliente(db.Model):
    __tablename__ = "clientes"
    id = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String,nullable=False)
    telefono = db.Column(db.Integer,nullable=False)
    email = db.Column(db.String,nullable=False)
    direccion = db.Column(db.String,nullable=False)
    fecha_registro = db.Column(db.DateTime,default=datetime.utcnow)

    difunto = db.relationship('Difunto', back_populates='cliente', lazy=True, cascade="all, delete-orphan")
    servicios = db.relationship('Servicio', back_populates='cliente', lazy=True, cascade="all, delete-orphan")
    pagos = db.relationship('Pago', back_populates='cliente', lazy=True, cascade="all, delete-orphan")
    contratos = db.relationship('Contrato', back_populates='cliente', cascade="all, delete-orphan")
    
    def __init__(self, nombre, telefono, email, direccion):
        self.nombre = nombre
        self.telefono = telefono
        self.email = email
        self.direccion = direccion

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Cliente.query.all()
    
    @staticmethod
    def get_by_id(id):
        return Cliente.query.get(id)
    
    
    def update(self, nombre=None, telefono=None, email=None, direccion=None):
        if nombre and telefono and email and direccion:
            self.nombre = nombre
            self.telefono = telefono
            self.email = email
            self.direccion = direccion
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        