from flask import Blueprint, request, jsonify
from src.models.productos import Producto
from src.models import session


productos_bp = Blueprint("productos", __name__)

@productos_bp.route("", methods=["POST"])
def crear_producto():
    data = request.get_json()
    nuevo_producto = Producto(
        nombre=data["nombre"], 
        descripcion=data.get("descripcion"), 
        precio=data["precio"], 
        stock=data.get("stock", 0), 
        material=data.get("material"), 
        dimensiones=data.get("dimensiones"),
        color=data.get("color"), 
        peso=data.get("peso"),
        imagen_principal=data.get("imagen_principal"),
        id_categoria=data["id_categoria"]
    )
    session.add(nuevo_producto)
    session.commit()
    return jsonify({"message": "Producto creado exitosamente"}), 201

@productos_bp.route("/<int:id_producto>", methods=["GET"])
def obtener_producto(id_producto):
    producto = session.query(Producto).filter(Producto.id_producto == id_producto).first()

    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404

    return jsonify({
        "id": producto.id_producto,
        "nombre": producto.nombre,
        "descripcion": producto.descripcion,
        "precio": producto.precio,
        "stock": producto.stock,
        "material": producto.material,
        "color": producto.color,
        "dimensiones": producto.dimensiones,
        "peso": producto.peso,
        "imagen_principal": producto.imagen_principal,
        "activo": producto.activo,
        "id_categoria": producto.id_categoria
    }), 200

@productos_bp.route("/<int:id_producto>", methods=["PUT"])
def actualizar_producto(id_producto):
    producto = session.query(Producto).filter(Producto.id_producto == id_producto).first()

    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404

    data = request.get_json()
    producto.nombre = data.get("nombre",producto.nombre)
    producto.descripcion = data.get("descripcion",producto.descripcion)
    producto.precio = data.get("precio",producto.precio)
    producto.stock = data.get("stock",producto.stock)
    producto.material = data.get("material",producto.material)
    producto.color = data.get("color",producto.color)
    producto.dimensiones = data.get("dimensiones",producto.dimensiones)
    producto.peso = data.get("peso",producto.peso)
    producto.id_categoria = data.get("id_categoria",producto.id_categoria)

    session.add(producto)
    session.commit()
    return jsonify({"message": "Producto actualizado exitosamente", "id_producto": producto.id_producto}), 200

@productos_bp.route("/<int:id_producto>", methods=["DELETE"])
def eliminar_producto(id_producto):
    producto = session.query(Producto).filter(Producto.id_producto == id_producto).first()

    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404

    session.delete(producto)
    session.commit()
    return jsonify({"message": "Producto eliminado exitosamente"}), 200

@productos_bp.route("", methods=["GET"])
def listar_productos():

    # Página actual
    page = request.args.get("page", 1, type=int)

    # Cantidad de productos por página
    per_page = request.args.get("per_page", 8, type=int)

    # Categoría opcional
    id_categoria = request.args.get("id_categoria", type=int)

    # Evitar valores inválidos
    if page < 1:
        page = 1

    if per_page < 1:
        per_page = 8

    # Consulta base
    query = session.query(Producto)

    # Filtrar por categoría si se solicita
    if id_categoria:
        query = query.filter(
            Producto.id_categoria == id_categoria
        )

    # Cantidad total de productos
    total_productos = query.count()

    # Calcular cantidad de páginas
    total_paginas = (total_productos + per_page - 1) // per_page

    # Obtener solamente los productos de la página actual
    productos = query.offset(
        (page - 1) * per_page
    ).limit(
        per_page
    ).all()

    productos_list = [

        {
            "id": producto.id_producto,
            "nombre": producto.nombre,
            "descripcion": producto.descripcion,
            "precio": producto.precio,
            "stock": producto.stock,
            "material": producto.material,
            "color": producto.color,
            "imagen_principal": producto.imagen_principal,
            "activo": producto.activo,
            "id_categoria": producto.id_categoria
        }

        for producto in productos

    ]

    return jsonify({
        "productos": productos_list,
        "pagina": page,
        "por_pagina": per_page,
        "total_productos": total_productos,
        "total_paginas": total_paginas
    }), 200