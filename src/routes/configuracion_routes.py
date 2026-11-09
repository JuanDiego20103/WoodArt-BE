from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError

from src.models import session
from src.utils.auth import token_required, rol_required
from src.utils.configuracion import (
    CONFIGURACION_DEFECTO,
    obtener_configuracion,
    guardar_configuracion
)

configuracion_bp = Blueprint("configuracion", __name__)


# =========================================================
# CONFIGURACIÓN PÚBLICA (la usa la tienda, no requiere token)
# =========================================================

@configuracion_bp.route("/publica", methods=["GET"])
def configuracion_publica():

    try:
        return jsonify(obtener_configuracion(solo_publica=True)), 200

    except SQLAlchemyError:
        session.rollback()
        return jsonify({"error": "No se pudo leer la configuración"}), 500


# =========================================================
# CONFIGURACIÓN COMPLETA (solo administradores)
# =========================================================

@configuracion_bp.route("", methods=["GET"])
@token_required
@rol_required("admin")
def ver_configuracion():

    try:
        valores = obtener_configuracion()

    except SQLAlchemyError:
        session.rollback()
        return jsonify({"error": "No se pudo leer la configuración"}), 500

    campos = [
        {
            "clave": clave,
            "valor": valores[clave],
            "tipo": info["tipo"],
            "etiqueta": info["etiqueta"],
            "descripcion": info["descripcion"]
        }
        for clave, info in CONFIGURACION_DEFECTO.items()
    ]

    return jsonify({"configuracion": campos}), 200


# =========================================================
# ACTUALIZAR CONFIGURACIÓN (solo administradores)
# =========================================================

@configuracion_bp.route("", methods=["PUT"])
@token_required
@rol_required("admin")
def actualizar_configuracion():

    data = request.get_json(silent=True)

    if not isinstance(data, dict) or not data:
        return jsonify({"error": "No se recibieron datos"}), 400

    try:
        configuracion, errores = guardar_configuracion(data)

    except SQLAlchemyError:
        session.rollback()
        return jsonify({"error": "No se pudo guardar la configuración"}), 500

    if errores:
        return jsonify({"error": " | ".join(errores)}), 400

    return jsonify({
        "message": "Configuración actualizada correctamente",
        "configuracion": configuracion
    }), 200
