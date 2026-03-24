from main import app
from extensiones import db
from models import User

with app.app_context():
    # CREACION DE LAS TABLAS PORQUE NO EXISTIAN
    db.create_all()
    
    # CREACION DE UN USUARIO ADMINISTRADOR
    nuevo_usuario = User(username='admin')
    nuevo_usuario.password = '1234'
    
    db.session.add(nuevo_usuario)
    db.session.commit()
    print("Usuario 'admin' creado con éxito.")