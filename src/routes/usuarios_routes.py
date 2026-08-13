from flask import Blueprint, request, jsonify
from src.models.usuarios import Usuario
from src.models import session

usuarios_bp = Blueprint("usuarios", __name__)


# =========================
# CREAR USUARIO
# =========================

@usuarios_bp.route("", methods=["POST"])
def crear_usuario():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No se recibieron datos"
        }), 400

    if not data.get("nombre"):
        return jsonify({
            "error": "El nombre es obligatorio"
        }), 400

    if not data.get("apellido"):
        return jsonify({
            "error": "El apellido es obligatorio"
        }), 400

    if not data.get("email"):
        return jsonify({
            "error": "El email es obligatorio"
        }), 400

    if not data.get("password"):
        return jsonify({
            "error": "La contraseña es obligatoria"
        }), 400

    # Verificar si el correo ya existe
    usuario_existente = session.query(Usuario).filter(
        Usuario.email == data["email"]
    ).first()

    if usuario_existente:
        return jsonify({
            "error": "El correo electrónico ya está registrado"
        }), 409

    nuevo_usuario = Usuario(

        nombre=data["nombre"],
        apellido=data["apellido"],
        email=data["email"],
        telefono=data.get("telefono"),
        password=data["password"],
        rol=data.get("rol", "cliente")

    )

    session.add(nuevo_usuario)
    session.commit()

    return jsonify({
        "message": "Usuario creado exitosamente",
        "usuario": {
            "id_usuario": nuevo_usuario.id_usuario,
            "nombre": nuevo_usuario.nombre,
            "apellido": nuevo_usuario.apellido,
            "email": nuevo_usuario.email,
            "telefono": nuevo_usuario.telefono,
            "rol": nuevo_usuario.rol
        }
    }), 201


# =========================
# OBTENER USUARIO
# =========================

@usuarios_bp.route("/<int:id_usuario>", methods=["GET"])
def obtener_usuario(id_usuario):

    usuario = session.query(Usuario).filter(
        Usuario.id_usuario == id_usuario
    ).first()

    if not usuario:
        return jsonify({
            "error": "Usuario no encontrado"
        }), 404

    return jsonify({
        "id_usuario": usuario.id_usuario,
        "nombre": usuario.nombre,
        "apellido": usuario.apellido,
        "email": usuario.email,
        "telefono": usuario.telefono,
        "rol": usuario.rol
    }), 200


# =========================
# ACTUALIZAR USUARIO
# =========================

@usuarios_bp.route("/<int:id_usuario>", methods=["PUT"])
def actualizar_usuario(id_usuario):

    usuario = session.query(Usuario).filter(
        Usuario.id_usuario == id_usuario
    ).first()

    if not usuario:
        return jsonify({
            "error": "Usuario no encontrado"
        }), 404

    data = request.get_json()

    usuario.nombre = data.get("nombre", usuario.nombre)
    usuario.apellido = data.get("apellido", usuario.apellido)
    usuario.email = data.get("email", usuario.email)
    usuario.telefono = data.get("telefono", usuario.telefono)
    usuario.password = data.get("password", usuario.password)
    usuario.rol = data.get("rol", usuario.rol)

    session.commit()

    return jsonify({
        "message": "Usuario actualizado exitosamente",
        "id_usuario": usuario.id_usuario
    }), 200


# =========================
# ELIMINAR USUARIO
# =========================

@usuarios_bp.route("/<int:id_usuario>", methods=["DELETE"])
def eliminar_usuario(id_usuario):

    usuario = session.query(Usuario).filter(
        Usuario.id_usuario == id_usuario
    ).first()

    if not usuario:
        return jsonify({
            "error": "Usuario no encontrado"
        }), 404

    session.delete(usuario)
    session.commit()

    return jsonify({
        "message": "Usuario eliminado exitosamente"
    }), 200


# =========================
# LISTAR USUARIOS
# =========================

@usuarios_bp.route("/", methods=["GET"])
def listar_usuarios():

    usuarios = session.query(Usuario).all()

    usuarios_list = [

        {
            "id_usuario": usuario.id_usuario,
            "nombre": usuario.nombre,
            "apellido": usuario.apellido,
            "email": usuario.email,
            "telefono": usuario.telefono,
            "rol": usuario.rol
        }

        for usuario in usuarios

    ]

    return jsonify(usuarios_list), 200


# =========================
# INICIAR SESIÓN
# =========================

@usuarios_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "error": "El email y la contraseña son obligatorios"
        }), 400

    usuario = session.query(Usuario).filter(
        Usuario.email == email
    ).first()

    if not usuario:
        return jsonify({
            "error": "Credenciales incorrectas"
        }), 401

    if usuario.password != password:
        return jsonify({
            "error": "Credenciales incorrectas"
        }), 401

    return jsonify({
        "message": "Inicio de sesión exitoso",
        "usuario": {
            "id_usuario": usuario.id_usuario,
            "nombre": usuario.nombre,
            "apellido": usuario.apellido,
            "email": usuario.email,
            "telefono": usuario.telefono,
            "rol": usuario.rol
        }
    }), 200