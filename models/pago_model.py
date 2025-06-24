from datetime import datetime
from database import db

class Pago(db.Model):
    __tablename__ = "pagos"
    id = db.Column(db.Integer,primary_key=True)
    cliente_id = db.Column(db.Integer,db.ForeignKey('clientes.id'),nullable=False)
    servicio_id = db.Column(db.Integer,db.ForeignKey('servicios.id'),nullable=False)
    monto = db.Column(db.Float(11,2),nullable=False)
    metodo_pago = db.Column(db.String,nullable=True)
    referencia = db.Column(db.String,nullable=True)
    fecha = db.Column(db.DateTime,default=datetime.utcnow)
    
    cliente = db.relationship('Cliente', back_populates='pagos')
    servicio = db.relationship('Servicio', back_populates='pagos')


    def __init__(self, cliente_id, servicio_id, monto, metodo_pago, referencia):
        self.cliente_id = cliente_id
        self.servicio_id = servicio_id
        self.monto = monto
        self.metodo_pago = metodo_pago
        self.referencia = referencia

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Pago.query.all()
    
    @staticmethod
    def get_by_id(id):
        return Pago.query.get(id)
    
    def update(self, cliente_id=None, servicio_id=None, monto=None, metodo_pago=None, referencia=None):
        if cliente_id and servicio_id and monto and metodo_pago and referencia:
            self.cliente_id = cliente_id
            self.servicio_id = servicio_id
            self.monto = monto
            self.metodo_pago = metodo_pago
            self.cliente_id = cliente_id
            self.referencia = referencia
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        