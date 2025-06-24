from datetime import datetime
from database import db

class Servicio(db.Model):
    __tablename__ = "servicios"
    id = db.Column(db.Integer,primary_key=True)
    tipo = db.Column(db.String,nullable=False)
    descripcion = db.Column(db.String,nullable=False)
    fecha = db.Column(db.Date,nullable=False)
    hora = db.Column(db.Time,nullable=False)
    cliente_id = db.Column(db.Integer,db.ForeignKey('clientes.id'),nullable=False)
    difunto_id = db.Column(db.Integer,db.ForeignKey('difuntos.id'),nullable=False)
    espacio_id = db.Column(db.Integer,db.ForeignKey('espacios.id'),nullable=True)
    costo = db.Column(db.Float(11,2),nullable=False)
    estado = db.Column(db.String ,nullable=True)

    cliente = db.relationship('Cliente', back_populates='servicios')
    difunto = db.relationship('Difunto', back_populates='servicios')
    espacio = db.relationship('Espacio', back_populates='servicios')
    pagos = db.relationship('Pago', back_populates='servicio')


    def __init__(self, tipo, descripcion, fecha, hora, cliente_id, difunto_id, espacio_id, costo, estado):
        self.tipo = tipo
        self.descripcion = descripcion
        self.fecha = fecha
        self.hora = hora
        self.cliente_id = cliente_id
        self.difunto_id = difunto_id
        self.espacio_id = espacio_id
        self.costo = costo
        self.estado = estado

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Servicio.query.all()
    
    @staticmethod
    def get_by_id(id):
        return Servicio.query.get(id)
    
    def update(self, tipo=None, descripcion=None, fecha=None, hora=None, cliente_id=None, difunto_id=None, espacio_id=None, costo=None, estado=None):
        if tipo and descripcion and fecha and hora and cliente_id and difunto_id and espacio_id and costo and estado:
            self.tipo = tipo
            self.descripcion = descripcion
            self.fecha = fecha
            self.hora = hora
            self.cliente_id = cliente_id
            self.difunto_id = difunto_id
            self.espacio_id = espacio_id
            self.costo = costo
            self.estado = estado
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        