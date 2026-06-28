from flask import Blueprint, request, jsonify , session as flask_session
from src.models.direcciones import Direccion
from src.models import session as db_session

direcciones_bp = Blueprint('direcciones', __name__)

@direcciones_bp.route("",methods=["POST"])
def crear_direccion():


    data = request.get_json()
    direccion = data.get("direccion")
    ciudad = data.get("ciudad")
    departamento = data.get("departamento")
    codigo_postal = data.get("codigo_postal")
    pais = data.get("pais")
    id_usuario=data.get("id_usuario")

    nueva_direccion = Direccion(
        direccion=direccion,
        ciudad=ciudad,
        departamento=departamento,
        codigo_postal=codigo_postal,
        pais=pais,
        id_usuario=id_usuario
    )

    try:
        print(nueva_direccion)
        print(type(nueva_direccion))
        db_session.add(nueva_direccion)
        db_session.commit()
        return jsonify({"message": "Dirección creada exitosamente","id_direccion": nueva_direccion.id_direccion}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@direcciones_bp.route("",methods=["GET"])
def obtener_direcciones():
    if "id_usuario" not in flask_session:
        return jsonify({"error": "Usuario no autenticado"}), 401

    direcciones = Direccion.get_by_user_id(flask_session["id_usuario"])
    return jsonify({"direcciones": [dir.to_dict() for dir in direcciones]}), 200

@direcciones_bp.route("/<int:id_direccion>",methods=["GET"])
def obtener_direccion(id_direccion):
    if "id_usuario" not in flask_session:
        return jsonify({"error": "Usuario no autenticado"}), 401

    direccion = Direccion.get_by_id_and_user(id_direccion, flask_session["id_usuario"])
    if not direccion:
        return jsonify({"error": "Dirección no encontrada"}), 404

    return jsonify({"direccion": direccion.to_dict()}), 200

@direcciones_bp.route("/<int:id_direccion>",methods=["PUT"])
def actualizar_direccion(id_direccion):
    if "id_usuario" not in flask_session:
        return jsonify({"error": "Usuario no autenticado"}), 401

    data = request.get_json()
    direccion = data.get("direccion")
    ciudad = data.get("ciudad")
    departamento = data.get("departamento")
    codigo_postal = data.get("codigo_postal")
    pais = data.get("pais")

    direccion_obj = Direccion.get_by_id_and_user(id_direccion, flask_session["id_usuario"])
    if not direccion_obj:
        return jsonify({"error": "Dirección no encontrada"}), 404

    direccion_obj.direccion = direccion
    direccion_obj.ciudad = ciudad
    direccion_obj.departamento = departamento
    direccion_obj.codigo_postal = codigo_postal
    direccion_obj.pais = pais

    try:
        db_session.add(direccion_obj)
        db_session.commit()
        return jsonify({"message": "Dirección actualizada exitosamente", "direccion": direccion_obj.to_dict()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@direcciones_bp.route("/<int:id_direccion>",methods=["DELETE"])
def eliminar_direccion(id_direccion):
    if "id_usuario" not in flask_session:
        return jsonify({"error": "Usuario no autenticado"}), 401

    direccion = Direccion.get_by_id_and_user(id_direccion, flask_session["id_usuario"])
    if not direccion:
        return jsonify({"error": "Dirección no encontrada"}), 404

    try:
        db_session.delete(direccion)
        db_session.commit()
        return jsonify({"message": "Dirección eliminada exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500    