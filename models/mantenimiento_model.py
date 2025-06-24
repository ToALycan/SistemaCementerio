from datetime import datetime
from database import db

class Mantenimiento(db.Model):
    __tablename__ = "mantenimientos"
    id = db.Column(db.Integer, primary_key=True)
    espacio_id = db.Column(db.Integer, db.ForeignKey('espacios.id'), nullable=False)
    descripcion = db.Column(db.String, nullable=False)
    fecha_programada = db.Column(db.Date, nullable=False)
    fecha_realizado = db.Column(db.Date, nullable=True)  # Acepta valores nulos
    costo = db.Column(db.Float(11,2), nullable=False)
    estado = db.Column(db.String, nullable=True)
    
    espacio = db.relationship('Espacio', back_populates='mantenimiento')

    def __init__(self, espacio_id, descripcion, fecha_programada, costo, estado, fecha_realizado=None):
        self.espacio_id = espacio_id
        self.descripcion = descripcion
        self.fecha_programada = fecha_programada
        self.costo = costo
        self.estado = estado
        self.fecha_realizado = fecha_realizado  # Ahora es opcional

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Mantenimiento.query.all()
    
    @staticmethod
    def get_by_id(id):
        return Mantenimiento.query.get(id)
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key) and value is not None:
                setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()