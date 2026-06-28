from flask import Blueprint, request, jsonify
from src.models.usuarios import Usuario
from src.models import session

usuarios_bp = Blueprint("usuarios",__name__)

@usuarios_bp.route("/", methods=["POST"])
def crear_usuario():

    data = request.get_json()

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
        "message": "Usuario creado exitosamente"
    }), 201

@usuarios_bp.route("/<int:id_usuario>", methods=["GET"])
def obtener_usuario(id_usuario):

    usuario = session.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()

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

@usuarios_bp.route("/<int:id_usuario>", methods=["PUT"])
def actualizar_usuario(id_usuario):
    usuario = session.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()

    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    data = request.get_json()
    usuario.nombre = data.get("nombre", usuario.nombre)
    usuario.apellido = data.get("apellido", usuario.apellido)
    usuario.email = data.get("email", usuario.email)
    usuario.telefono = data.get("telefono", usuario.telefono)
    usuario.password = data.get("password", usuario.password)
    usuario.rol = data.get("rol", usuario.rol)

    session.commit()
    return jsonify({"message": "Usuario actualizado exitosamente", "id_usuario": usuario.id_usuario
}), 200

@usuarios_bp.route("/<int:id_usuario>", methods=["DELETE"])
def eliminar_usuario(id_usuario):

    usuario = session.query( Usuario).filter(Usuario.id_usuario == id_usuario).first()

    if not usuario:

        return jsonify({"error": "Usuario no encontrado"}), 404

    session.delete(usuario)

    session.commit()

    return jsonify({"message": "Usuario eliminado exitosamente"}), 200

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

    return jsonify(
        usuarios_list
    ), 200