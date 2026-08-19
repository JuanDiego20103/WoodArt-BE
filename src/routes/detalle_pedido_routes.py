from flask import Blueprint, request, jsonify
from src.models.detalle_pedido import DetallePedido
from src.utils.auth import token_required, rol_required

detalle_pedido_bp = Blueprint('detalle_pedido_bp', __name__)


@detalle_pedido_bp.route('/detalle_pedido/<int:id>', methods=['GET'])
def get_detalle_pedido(id):
    # Aquí deberías agregar el código para obtener el DetallePedido de la base de datos usando el id
    detalle_pedido = None  # Reemplaza esto con la consulta a la base de datos
    if detalle_pedido:
        return jsonify({
            'id_detalle': detalle_pedido.id_detalle,
            'cantidad': detalle_pedido.cantidad,
            'precio_unitario': detalle_pedido.precio_unitario,
            'subtotal': detalle_pedido.subtotal,
            'id_pedido': detalle_pedido.id_pedido,
            'id_producto': detalle_pedido.id_producto
        }), 200
    else:
        return jsonify({'message': 'DetallePedido no encontrado'}), 404
    
    
@detalle_pedido_bp.route('/detalle_pedido', methods=['GET'])
def get_all_detalles_pedido():
    # Aquí deberías agregar el código para obtener todos los DetallePedido de la base de datos
    detalles_pedido = []  # Reemplaza esto con la consulta a la base de datos
    return jsonify([{
        'id_detalle': detalle.id_detalle,
        'cantidad': detalle.cantidad,
        'precio_unitario': detalle.precio_unitario,
        'subtotal': detalle.subtotal,
        'id_pedido': detalle.id_pedido,
        'id_producto': detalle.id_producto
    } for detalle in detalles_pedido]), 200