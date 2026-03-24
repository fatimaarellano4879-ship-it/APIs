from flask import Blueprint, jsonify, request
from models import Juego

from extensiones import db 

# Blueprint
api_blueprint = Blueprint('api', __name__)

# Obtener juegos
@api_blueprint.route('/juegos', methods=['GET'])
def get_juegos():
    juegos = Juego.query.all()
    return jsonify([juego.to_json() for juego in juegos]), 200

# Crear juego
@api_blueprint.route('/juegos', methods=['POST'])
def create_juego():
    data = request.get_json()
    
    if not data or not 'nombre' in data or not 'precio' in data:
        return jsonify({'error': 'Faltan datos'}), 400 
        
    nuevo_juego = Juego(
        nombre=data['nombre'],
        descripcion=data.get('descripcion', 'Sin descripción'),
        precio=data['precio']
    )
    db.session.add(nuevo_juego)
    db.session.commit()
    
    return jsonify(nuevo_juego.to_json()), 201

# Filtrar Juego
@api_blueprint.route('/juegos/<int:id>', methods=['GET'])
def get_juego(id):
    juego = Juego.query.get_or_404(id)
    return jsonify(juego.to_json()), 200

# Modificar Juego
@api_blueprint.route('/juegos/<int:id>', methods=['PUT'])
def update_juego(id):
    juego = Juego.query.get_or_404(id)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Cuerpo de la petición vacío'}), 400
        
    juego.nombre = data.get('nombre', juego.nombre)
    juego.descripcion = data.get('descripcion', juego.descripcion)
    juego.precio = data.get('precio', juego.precio)
    
    db.session.commit()
    return jsonify(juego.to_json()), 200

# Eliminar Juego
@api_blueprint.route('/juegos/<int:id>', methods=['DELETE'])
def delete_juego(id):
    juego = Juego.query.get_or_404(id)
    db.session.delete(juego)
    db.session.commit()
    return '', 204