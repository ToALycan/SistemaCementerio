from datetime import datetime
from database import db

class Contrato(db.Model):
    __tablename__ = "contratos"
    id = db.Column(db.Integer,primary_key=True)
    cliente_id = db.Column(db.Integer,db.ForeignKey('clientes.id'),nullable=False)
    espacio_id = db.Column(db.Integer,db.ForeignKey('espacios.id'),nullable=False)
    fecha_inicio = db.Column(db.DateTime,nullable=False)
    fecha_fin = db.Column(db.String,nullable=True)
    tipo = db.Column(db.String,nullable=False)
    costo = db.Column(db.Float(11,2),nullable=False)
    estado = db.Column(db.String,nullable=False)

    
    cliente = db.relationship('Cliente', back_populates='contratos')
    espacio = db.relationship('Espacio', back_populates='contratos')


    def __init__(self, cliente_id, espacio_id, fecha_inicio, fecha_fin, tipo, costo, estado):
        self.cliente_id = cliente_id
        self.espacio_id = espacio_id
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.tipo = tipo
        self.costo = costo
        self.estado = estado

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Contrato.query.all()
    
    @staticmethod
    def get_by_id(id):
        return Contrato.query.get(id)
    
    def update(self, cliente_id=None, espacio_id=None, fecha_inicio=None, fecha_fin=None, tipo=None, costo=None, estado=None):
        if cliente_id and espacio_id and fecha_inicio and fecha_fin and tipo and costo and estado:
            self.cliente_id = cliente_id
            self.espacio_id = espacio_id
            self.fecha_inicio = fecha_inicio
            self.fecha_fin = fecha_fin
            self.tipo = tipo
            self.costo = costo
            self.estado = estado
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
