from flask import Blueprint, request, jsonify
from src.models.categorias import Categoria
from src.models import session
from src.utils.auth import token_required, rol_required


categorias_bp = Blueprint("categorias", __name__)

@categorias_bp.route("", methods=["POST"])
def crear_categoria():
    data = request.get_json()
    nombre = data.get("nombre")
    descripcion = data.get("descripcion")

    if not nombre:
        return jsonify({'error': 'El nombre es obligatorio'}), 400

    nueva_categoria = Categoria(nombre=nombre, descripcion=descripcion)
    session.add(nueva_categoria)
    session.commit()

    return jsonify({'message': 'Categoría creada exitosamente', 'id_categoria': nueva_categoria.id_categoria}), 201

@categorias_bp.route("/", methods=["GET"])
def obtener_categorias():
    categorias = session.query(Categoria).all()
    categorias_list = [{'id_categoria': cat.id_categoria, 'nombre': cat.nombre, 'descripcion': cat.descripcion} for cat in categorias]
    return jsonify(categorias_list), 200

@categorias_bp.route("/<int:id_categoria>", methods=["GET"])
def obtener_categoria(id_categoria):
    categoria = session.query(Categoria).filter_by(id_categoria=id_categoria).first()
    if not categoria:
        return jsonify({'error': 'Categoría no encontrada'}), 404

    categoria_data = {'id_categoria': categoria.id_categoria, 'nombre': categoria.nombre, 'descripcion': categoria.descripcion}
    return jsonify(categoria_data), 200

@categorias_bp.route("/<int:id_categoria>", methods=["PUT"])
def actualizar_categoria(id_categoria):
    categoria = session.query(Categoria).filter_by(id_categoria=id_categoria).first()
    if not categoria:
        return jsonify({'error': 'Categoría no encontrada'}), 404

    data = request.get_json()
    nombre = data.get("nombre")
    descripcion = data.get("descripcion")

    if nombre:
        categoria.nombre = nombre
    if descripcion:
        categoria.descripcion = descripcion

    session.commit()
    return jsonify({'message': 'Categoría actualizada exitosamente'}), 200