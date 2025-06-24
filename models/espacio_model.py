from datetime import datetime
from database import db

class Espacio(db.Model):
    __tablename__ = "espacios"
    id = db.Column(db.Integer,primary_key=True)
    numero = db.Column(db.String,nullable=False)
    tipo = db.Column(db.String,nullable=False)
    descripcion = db.Column(db.String,nullable=False)
    sector = db.Column(db.String,nullable=False)
    pabellon = db.Column(db.String,nullable=False)
    fila = db.Column(db.String,nullable=False)
    estado = db.Column(db.String,nullable=False)
    fecha_ocupacion = db.Column(db.DateTime,nullable=True)
    difunto_id = db.Column(db.Integer,db.ForeignKey('difuntos.id') ,nullable=True)

    difunto = db.relationship('Difunto', back_populates='espacio')
    servicios = db.relationship('Servicio', back_populates='espacio')
    mantenimiento = db.relationship('Mantenimiento', back_populates='espacio')
    contratos = db.relationship('Contrato', back_populates='espacio')


    def __init__(self, numero, tipo, descripcion, sector, pabellon, fila, estado, fecha_ocupacion, difunto_id):
        self.numero = numero
        self.tipo = tipo
        self.descripcion = descripcion
        self.sector = sector
        self.pabellon = pabellon
        self.fila = fila
        self.estado = estado
        self.fecha_ocupacion = fecha_ocupacion
        self.difunto_id = difunto_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Espacio.query.all()
    
    @staticmethod
    def get_by_id(id):
        return Espacio.query.get(id)
    
    def update(self, numero=None, tipo=None, descripcion=None, sector=None, pabellon=None, fila=None, estado=None, fecha_ocupacion=None, difunto_id=None):
        if numero and tipo and descripcion and sector and pabellon and fila and estado and fecha_ocupacion and difunto_id:
            self.numero = numero
            self.tipo = tipo
            self.descripcion = descripcion
            self.sector = sector
            self.pabellon = pabellon
            self.fila = fila
            self.estado = estado
            self.fecha_ocupacion = fecha_ocupacion
            self.difunto_id = difunto_id
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        