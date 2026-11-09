from flask import Blueprint, request, jsonify, session
from src.models.carrito import Carrito
from src.models.productos import Producto
from src.models import session
from src.utils.auth import token_required, rol_required

carrito_bp = Blueprint('carrito', __name__)

@carrito_bp.route("", methods=["POST"])
@token_required
def agregar_al_carrito():

    data = request.get_json()

    id_usuario = data.get("id_usuario")
    id_producto = data.get("id_producto")
    cantidad = data.get("cantidad", 1)

    if not id_usuario:
        return jsonify({
            "error": "Usuario no autenticado"
        }), 401

    if not id_producto:
        return jsonify({
            "error": "Producto no especificado"
        }), 400

    # Si el producto ya está en el carrito, solo se suma la cantidad
    item = session.query(Carrito).filter(
        Carrito.id_usuario == id_usuario,
        Carrito.id_producto == id_producto
    ).first()

    if item:
        item.cantidad = (item.cantidad or 0) + cantidad
    else:
        session.add(Carrito(
            cantidad=cantidad,
            id_usuario=id_usuario,
            id_producto=id_producto
        ))

    session.commit()

    return jsonify({
        "message": "Producto agregado al carrito"
    }), 201

@carrito_bp.route("", methods=["GET"])
@token_required
def obtener_carrito():

    id_usuario = request.args.get("id_usuario", type=int)

    if not id_usuario:
        return jsonify({
            "error": "Usuario no autenticado"
        }), 401

    items_carrito = session.query(Carrito, Producto).join(
        Producto,
        Carrito.id_producto == Producto.id_producto
    ).filter(
        Carrito.id_usuario == id_usuario
    ).all()

    carrito = []

    for item, producto in items_carrito:

        carrito.append({
            "id_carrito": item.id_carrito,
            "id_producto": producto.id_producto,
            "nombre": producto.nombre,
            "precio": producto.precio,
            "cantidad": item.cantidad,
            "imagen_principal": producto.imagen_principal,
            "subtotal": producto.precio * item.cantidad
        })

    return jsonify(carrito), 200

@carrito_bp.route("/<int:id_carrito>", methods=["DELETE"])
@token_required
def eliminar_del_carrito(id_carrito):

    # Solo se puede borrar un producto del carrito del usuario del token
    item = session.query(Carrito).filter(
        Carrito.id_carrito == id_carrito,
        Carrito.id_usuario == request.usuario.id_usuario
    ).first()

    if not item:
        return jsonify({
            "error": "El producto no está en tu carrito"
        }), 404

    session.delete(item)
    session.commit()

    return jsonify({
        "message": "Producto eliminado del carrito"
    }), 200

@carrito_bp.route('/<int:id_producto>', methods=['PUT'])
@token_required
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
@token_required
def obtener_total_carrito():
    id_usuario = session.get('id_usuario')
    
    if not id_usuario:
        return jsonify({'error': 'Usuario no autenticado'}), 401
    
    # Aquí deberías calcular el total del carrito consultando la base de datos
    # total = session.query(func.sum(Carrito.cantidad * Producto.precio)).join(Producto).filter(Carrito.id_usuario == id_usuario).scalar()
    
    # Simulación de respuesta
    total = 100.00
    
    return jsonify({'total': total}), 200