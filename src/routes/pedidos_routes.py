from flask import Blueprint, request, jsonify
from src.models.pedidos import Pedido

pedidos_bp = Blueprint("pedidos",__name__)

@pedidos_bp.route("/pedidos",methods=["POST"])
def crear_pedido():
    data = request.get_json()
    nuevo_pedido = Pedido(
        id_usuario=data["id_usuario"],
        id_direccion=data["id_direccion"],
        detalles=data["detalles"],
        estado_pago=data["estado_pago"],
        fecha_pedido=data["fecha_pedido"],
        estado=data["estado"],
        total=data["total"]
    )
    nuevo_pedido.save()
    return jsonify({"message": "Pedido creado exitosamente"}), 201

@pedidos_bp.route("/pedidos/<int:id_pedido>", methods=["GET"])
def obtener_pedido(id_pedido):
    pedido = Pedido.query.get(id_pedido)

    if not pedido:
        return jsonify({"error": "Pedido no encontrado"}), 404

    return jsonify({
        "id_pedido": pedido.id_pedido,
        "id_usuario": pedido.id_usuario,
        "id_direccion": pedido.id_direccion,
        "detalles": pedido.detalles,
        "estado_pago": pedido.estado_pago,
        "fecha_pedido": pedido.fecha_pedido,
        "estado": pedido.estado,
        "total": pedido.total
    }), 200

@pedidos_bp.route("/pedidos/<int:id_pedido>", methods=["PUT"])
def actualizar_pedido(id_pedido):
    pedido = Pedido.query.get(id_pedido)

    if not pedido:
        return jsonify({"error": "Pedido no encontrado"}), 404

    data = request.get_json()
    pedido.id_usuario = data.get("id_usuario", pedido.id_usuario)
    pedido.id_direccion = data.get("id_direccion", pedido.id_direccion)
    pedido.detalles = data.get("detalles", pedido.detalles)
    pedido.estado_pago = data.get("estado_pago", pedido.estado_pago)
    pedido.fecha_pedido = data.get("fecha_pedido", pedido.fecha_pedido)
    pedido.estado = data.get("estado", pedido.estado)
    pedido.total = data.get("total", pedido.total)

    pedido.save()
    return jsonify({"message": "Pedido actualizado exitosamente", "id_pedido": pedido.id_pedido}), 200

@pedidos_bp.route("/pedidos", methods=["GET"])
def listar_pedidos():
    pedidos = Pedido.query.all()
    pedidos_list = []
    for pedido in pedidos:
        pedidos_list.append({
            "id_pedido": pedido.id_pedido,
            "id_usuario": pedido.id_usuario,
            "id_direccion": pedido.id_direccion,
            "detalles": pedido.detalles,
            "estado_pago": pedido.estado_pago,
            "fecha_pedido": pedido.fecha_pedido,
            "estado": pedido.estado,
            "total": pedido.total
        })
    return jsonify(pedidos_list), 200