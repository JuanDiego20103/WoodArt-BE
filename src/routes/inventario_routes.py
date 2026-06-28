from flask import Blueprint, request, jsonify
from src.models.inventario import MovimientoInventario

inventario_bp = Blueprint('inventario', __name__)

@inventario_bp.route('/movimientos', methods=['POST'])
def crear_movimiento():
    data = request.get_json()
    nuevo_movimiento = MovimientoInventario(
        tipo=data['tipo'],
        cantidad=data['cantidad'],
        descripcion=data['descripcion'],
        id_producto=data['id_producto']
    )
    # Aquí deberías agregar el nuevo_movimiento a la sesión de la base de datos y hacer commit
    return jsonify({'message': 'Movimiento creado exitosamente'}), 201

@inventario_bp.route('/movimientos', methods=['GET'])
def obtener_movimientos():
    # Aquí deberías consultar los movimientos de inventario desde la base de datos
    movimientos = MovimientoInventario.query.all()
    return jsonify([{
        'id_movimiento': movimiento.id_movimiento,
        'tipo': movimiento.tipo,
        'cantidad': movimiento.cantidad,
        'descripcion': movimiento.descripcion,
        'fecha': movimiento.fecha.isoformat(),
        'id_producto': movimiento.id_producto
    } for movimiento in movimientos]), 200

@inventario_bp.route('/movimientos/<int:id_movimiento>', methods=['GET'])
def obtener_movimiento(id_movimiento):
    # Aquí deberías consultar un movimiento específico por su ID desde la base de datos
    movimiento = MovimientoInventario.query.get(id_movimiento)
    if movimiento:
        return jsonify({
            'id_movimiento': movimiento.id_movimiento,
            'tipo': movimiento.tipo,
            'cantidad': movimiento.cantidad,
            'descripcion': movimiento.descripcion,
            'fecha': movimiento.fecha.isoformat(),
            'id_producto': movimiento.id_producto
        }), 200
    else:
        return jsonify({'message': 'Movimiento no encontrado'}), 404