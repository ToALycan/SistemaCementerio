from datetime import datetime
from flask_login import UserMixin
from database import db
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model, UserMixin):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String,nullable=False)
    username = db.Column(db.String,nullable=False)
    password = db.Column(db.String,nullable=False)
    rol = db.Column(db.String,nullable=False)
    fecha_registro = db.Column(db.DateTime,default=datetime.utcnow)
    

    def __init__(self, nombre, username, password, rol):
        self.nombre = nombre
        self.username = username
        self.password = self.hash_password(password)
        self.rol = rol


    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password, password)
    
    def set_password(self, password):
        self.password = self.hash_password(password)
        db.session.commit()
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Usuario.query.all()

    @staticmethod
    def get_by_id(id):
        return Usuario.query.get(id)
    
    @staticmethod
    def get_by_username(username):
        return Usuario.query.filter_by(username=username).first()
     
    def update(self, nombre=None, username=None, rol=None):
        if nombre:
            self.nombre = nombre
        if username:
            self.username = username
        if rol:
            self.rol = rol
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def reset_password(self, nuevo_password=None):
        self.password = self.hash_password(nuevo_password)
        db.session.commit()

    def change_password(self, actual_password, nueva_password):
        if not self.verify_password(actual_password):
            return False  # contraseña actual incorrecta
        self.set_password(nueva_password)
        return True
    