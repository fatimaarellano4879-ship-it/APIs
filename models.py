from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensiones import db

class Juego(db.Model):
    __tablename__ = "juegos"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    descripcion = db.Column(db.String(255))
    precio = db.Column(db.Float)

    def to_json(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio': float(self.precio)
        }

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))

    @property
    def password(self):
        raise AttributeError('La contraseña no es legible')

    @password.setter
    def password(self, pwd):
        self.password_hash = generate_password_hash(pwd)

    def verify_password(self, pwd):
        return check_password_hash(self.password_hash, pwd)