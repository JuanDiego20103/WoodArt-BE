from flask import Blueprint, request, jsonify
from src.models.imagen_productos import ImagenProducto
from src.utils.auth import token_required, rol_required

imagen_producto_bp = Blueprint("imagen_producto",__name__)

@imagen_producto_bp.route("/imagenes_productos",methods=["POST"])
def crear_imagen_producto():
    data = request.get_json()
    nueva_imagen_producto = ImagenProducto(
        id_producto=data["id_producto"],
        url=data["url"]
    )
    nueva_imagen_producto.save()
    return jsonify({"message": "Imagen de producto creada exitosamente"}), 201


@imagen_producto_bp.route("/imagenes_productos/<int:id_imagen_producto>", methods=["GET"])
def obtener_imagen_producto(id_imagen_producto):
    imagen_producto = ImagenProducto.query.get(id_imagen_producto)

    if not imagen_producto:
        return jsonify({"error": "Imagen de producto no encontrada"}), 404

    return jsonify({
        "id_imagen_producto": imagen_producto.id_imagen_producto,
        "id_producto": imagen_producto.id_producto,
        "url": imagen_producto.url
    }), 200

@imagen_producto_bp.route("/imagenes_productos/<int:id_imagen_producto>", methods=["PUT"])
def actualizar_imagen_producto(id_imagen_producto):
    imagen_producto = ImagenProducto.query.get(id_imagen_producto)

    if not imagen_producto:
        return jsonify({"error": "Imagen de producto no encontrada"}), 404

    data = request.get_json()
    imagen_producto.id_producto = data.get("id_producto", imagen_producto.id_producto)
    imagen_producto.url = data.get("url", imagen_producto.url)

    imagen_producto.save()
    return jsonify({"message": "Imagen de producto actualizada exitosamente", "id_imagen_producto": imagen_producto.id_imagen_producto
}), 200

@imagen_producto_bp.route("/imagenes_productos/<int:id_imagen_producto>", methods=["DELETE"])
def eliminar_imagen_producto(id_imagen_producto):
    imagen_producto = ImagenProducto.query.get(id_imagen_producto)

    if not imagen_producto:
        return jsonify({"error": "Imagen de producto no encontrada"}), 404

    imagen_producto.delete()
    return jsonify({"message": "Imagen de producto eliminada exitosamente"}), 200