from functools import wraps
from flask import request, jsonify
import jwt
import os

from src.models.usuarios import Usuario
from src.models import session

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")


def token_required(f):

    @wraps(f)
    def decorada(*args, **kwargs):

        auth = request.headers.get("Authorization", "")

        if not auth.startswith("Bearer "):
            return jsonify({
                "error": "Token faltante o mal formado"
            }), 401

        token = auth.split(" ", 1)[1].strip()

        try:
            payload = jwt.decode(
                token,
                JWT_SECRET_KEY,
                algorithms=["HS256"]
            )

        except jwt.ExpiredSignatureError:
            return jsonify({
                "error": "Token expirado, inicia sesión de nuevo"
            }), 401

        except jwt.InvalidTokenError:
            return jsonify({
                "error": "Token inválido"
            }), 401

        usuario = session.query(Usuario).filter(
            Usuario.id_usuario == payload["id_usuario"]
        ).first()

        if not usuario:
            return jsonify({
                "error": "Usuario no encontrado"
            }), 401

        request.usuario = usuario

        return f(*args, **kwargs)

    return decorada


def rol_required(*roles):

    def decorador(f):

        @wraps(f)
        def decorada(*args, **kwargs):

            if request.usuario.rol not in roles:
                return jsonify({
                    "error": "No tienes permisos para esta acción"
                }), 403

            return f(*args, **kwargs)

        return decorada

    return decorador