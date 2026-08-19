from flask import Blueprint, request, jsonify
from src.models.pagos import Pago
from src.utils.auth import token_required, rol_required

pagos_bp = Blueprint('pagos', __name__)

@pagos_bp.route('/pagos', methods=['POST'])
def crear_pago():
    data = request.get_json()
    nuevo_pago = Pago(
        metodo_pago=data['metodo_pago'],
        monto=data['monto'],
        estado=data['estado'],
        id_pedido=data['id_pedido']
    )
    # Aquí deberías agregar el nuevo pago a la base de datos y hacer commit
    return jsonify({'message': 'Pago creado exitosamente'}), 201

@pagos_bp.route('/pagos/<int:id_pago>', methods=['GET'])
def obtener_pago(id_pago):
    # Aquí deberías consultar el pago por su ID en la base de datos
    pago = Pago.query.get(id_pago)
    if pago:
        return jsonify({
            'id_pago': pago.id_pago,
            'metodo_pago': pago.metodo_pago,
            'monto': pago.monto,
            'estado': pago.estado,
            'fecha_pago': pago.fecha_pago.isoformat(),
            'id_pedido': pago.id_pedido
        })
    else:
        return jsonify({'message': 'Pago no encontrado'}), 404
    
@pagos_bp.route('/pagos/<int:id_pago>', methods=['PUT'])
def actualizar_pago(id_pago):
    data = request.get_json()
    pago = Pago.query.get(id_pago)
    if pago:
        pago.metodo_pago = data.get('metodo_pago', pago.metodo_pago)
        pago.monto = data.get('monto', pago.monto)
        pago.estado = data.get('estado', pago.estado)
        # Aquí deberías hacer commit de los cambios a la base de datos
        return jsonify({'message': 'Pago actualizado exitosamente'})
    else:
        return jsonify({'message': 'Pago no encontrado'}), 404
    
    
@pagos_bp.route('/pagos', methods=['GET'])
def listar_pagos():
    # Aquí deberías consultar todos los pagos en la base de datos
    pagos = Pago.query.all()
    return jsonify([{
        'id_pago': pago.id_pago,
        'metodo_pago': pago.metodo_pago,
        'monto': pago.monto,
        'estado': pago.estado,
        'fecha_pago': pago.fecha_pago.isoformat(),
        'id_pedido': pago.id_pedido
    } for pago in pagos])