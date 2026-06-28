from flask import Blueprint, request, jsonify, session
from src.models.carrito import Carrito

carrito_bp = Blueprint('carrito', __name__)

@carrito_bp.route('', methods=['POST'])
def agregar_al_carrito():
    data = request.get_json()
    id_usuario = session.get('id_usuario')
    
    if not id_usuario:
        return jsonify({'error': 'Usuario no autenticado'}), 401
    
    nuevo_item = Carrito(
        cantidad=data['cantidad'],
        id_usuario=id_usuario,
        id_producto=data['id_producto']
    )
    
    # Aquí deberías agregar el nuevo_item a la base de datos y hacer commit
    # session.add(nuevo_item)
    # session.commit()
    
    return jsonify({'message': 'Producto agregado al carrito'}), 201

@carrito_bp.route('', methods=['GET'])
def obtener_carrito():
    id_usuario = session.get('id_usuario')
    
    if not id_usuario:
        return jsonify({'error': 'Usuario no autenticado'}), 401
    
    # Aquí deberías consultar la base de datos para obtener los items del carrito del usuario
    # items_carrito = session.query(Carrito).filter_by(id_usuario=id_usuario).all()
    
    # Simulación de respuesta
    items_carrito = [
        {'id_producto': 1, 'cantidad': 2},
        {'id_producto': 2, 'cantidad': 1}
    ]
    
    return jsonify(items_carrito), 200

@carrito_bp.route('/<int:id_producto>', methods=['DELETE'])
def eliminar_del_carrito(id_producto):
    id_usuario = session.get('id_usuario')
    
    if not id_usuario:
        return jsonify({'error': 'Usuario no autenticado'}), 401
    
    # Aquí deberías eliminar el item del carrito de la base de datos
    # item = session.query(Carrito).filter_by(id_usuario=id_usuario, id_producto=id_producto).first()
    # if item:
    #     session.delete(item)
    #     session.commit()
    
    return jsonify({'message': 'Producto eliminado del carrito'}), 200

@carrito_bp.route('/<int:id_producto>', methods=['PUT'])
def actualizar_cantidad(id_producto):
    data = request.get_json()
    id_usuario = session.get('id_usuario')
    
    if not id_usuario:
        return jsonify({'error': 'Usuario no autenticado'}), 401
    
    # Aquí deberías actualizar la cantidad del item en la base de datos
    # item = session.query(Carrito).filter_by(id_usuario=id_usuario, id_producto=id_producto).first()
    # if item:
    #     item.cantidad = data['cantidad']
    #     session.commit()
    
    return jsonify({'message': 'Cantidad actualizada en el carrito'}), 200

@carrito_bp.route('/total', methods=['GET'])
def obtener_total_carrito():
    id_usuario = session.get('id_usuario')
    
    if not id_usuario:
        return jsonify({'error': 'Usuario no autenticado'}), 401
    
    # Aquí deberías calcular el total del carrito consultando la base de datos
    # total = session.query(func.sum(Carrito.cantidad * Producto.precio)).join(Producto).filter(Carrito.id_usuario == id_usuario).scalar()
    
    # Simulación de respuesta
    total = 100.00
    
    return jsonify({'total': total}), 200