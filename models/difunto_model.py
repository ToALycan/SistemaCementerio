from datetime import datetime
from database import db

class Difunto(db.Model):
    __tablename__ = "difuntos"
    id = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String,nullable=False)
    genero = db.Column(db.String,nullable=False)
    fecha_nacimiento = db.Column(db.DateTime,nullable=False)
    fecha_defuncion = db.Column(db.DateTime,nullable=False)
    cedula_identidad = db.Column(db.Integer,nullable=False)
    estado_civil = db.Column(db.String,nullable=False)
    causa_muerte = db.Column(db.String,nullable=True)
    cliente_id = db.Column(db.Integer,db.ForeignKey('clientes.id') ,nullable=False)

    cliente = db.relationship('Cliente', back_populates='difunto')
    espacio = db.relationship('Espacio',back_populates='difunto')
    servicios = db.relationship('Servicio',back_populates='difunto')

    def __init__(self, nombre, genero, fecha_nacimiento, fecha_defuncion, cedula_identidad, estado_civil, causa_muerte, cliente_id):
        self.nombre = nombre
        self.genero = genero
        self.fecha_nacimiento = fecha_nacimiento
        self.fecha_defuncion = fecha_defuncion
        self.cedula_identidad = cedula_identidad
        self.estado_civil = estado_civil
        self.causa_muerte = causa_muerte
        self.cliente_id = cliente_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Difunto.query.all()
    
    @staticmethod
    def get_by_id(id):
        return Difunto.query.get(id)
    
    def update(self, nombre=None, genero=None, fecha_nacimiento=None, fecha_defuncion=None, cedula_identidad=None, estado_civil=None, causa_muerte=None, cliente_id=None):
        if nombre and genero and fecha_nacimiento and fecha_defuncion and cedula_identidad and estado_civil and causa_muerte and cliente_id:
            self.nombre = nombre
            self.genero = genero
            self.fecha_nacimiento = fecha_nacimiento
            self.fecha_defuncion = fecha_defuncion
            self.cedula_identidad = cedula_identidad
            self.estado_civil = estado_civil
            self.causa_muerte = causa_muerte
            self.cliente_id = cliente_id
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        