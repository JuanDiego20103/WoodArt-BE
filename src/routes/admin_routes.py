from datetime import datetime, timedelta

from flask import Blueprint, request, jsonify
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

from src.models import session
from src.models.usuarios import Usuario
from src.models.productos import Producto
from src.models.categorias import Categoria
from src.models.pedidos import Pedido
from src.models.detalle_pedido import DetallePedido
from src.utils.auth import token_required, rol_required
from src.utils.configuracion import obtener_valor

admin_bp = Blueprint("admin", __name__)

# Estados de pedido que cuentan como venta realizada
ESTADOS_VENTA = ("pagado", "enviado", "entregado")
ESTADOS_PEDIDO = ("pendiente", "pagado", "enviado", "entregado", "cancelado")
MESES = ("Ene", "Feb", "Mar", "Abr", "May", "Jun",
         "Jul", "Ago", "Sep", "Oct", "Nov", "Dic")


def _fecha_texto(fecha):
    return fecha.strftime("%Y-%m-%d %H:%M") if fecha else None


# =========================================================
# ANALÍTICAS DEL SISTEMA
# =========================================================

@admin_bp.route("/estadisticas", methods=["GET"])
@token_required
@rol_required("admin")
def estadisticas():

    try:
        return jsonify(_calcular_estadisticas()), 200

    except SQLAlchemyError as e:
        session.rollback()
        print("Error calculando estadísticas:", e)
        return jsonify({"error": "No se pudieron calcular las estadísticas"}), 500


def _calcular_estadisticas():

    ahora = datetime.now()

    # ---------------- Usuarios ----------------
    total_usuarios = session.query(func.count(Usuario.id_usuario)).scalar() or 0

    total_admins = session.query(func.count(Usuario.id_usuario)).filter(
        Usuario.rol == "admin"
    ).scalar() or 0

    nuevos_usuarios_30d = session.query(func.count(Usuario.id_usuario)).filter(
        Usuario.fecha_registro >= ahora - timedelta(days=30)
    ).scalar() or 0

    # ---------------- Productos ----------------
    total_productos = session.query(func.count(Producto.id_producto)).scalar() or 0

    productos_activos = session.query(func.count(Producto.id_producto)).filter(
        Producto.activo.is_(True)
    ).scalar() or 0

    sin_stock = session.query(func.count(Producto.id_producto)).filter(
        func.coalesce(Producto.stock, 0) <= 0
    ).scalar() or 0

    valor_inventario = session.query(
        func.sum(Producto.precio * func.coalesce(Producto.stock, 0))
    ).scalar() or 0

    # ---------------- Pedidos y ventas ----------------
    total_pedidos = session.query(func.count(Pedido.id_pedido)).scalar() or 0

    ingresos = session.query(func.sum(Pedido.total)).filter(
        Pedido.estado.in_(ESTADOS_VENTA)
    ).scalar() or 0

    pedidos_vendidos = session.query(func.count(Pedido.id_pedido)).filter(
        Pedido.estado.in_(ESTADOS_VENTA)
    ).scalar() or 0

    ticket_promedio = (ingresos / pedidos_vendidos) if pedidos_vendidos else 0

    # Pedidos por estado (siempre con los 5 estados, aunque estén en 0)
    conteo_estados = dict(
        session.query(Pedido.estado, func.count(Pedido.id_pedido))
        .group_by(Pedido.estado)
        .all()
    )

    pedidos_por_estado = [
        {"estado": estado, "cantidad": conteo_estados.get(estado, 0)}
        for estado in ESTADOS_PEDIDO
    ]

    # Ventas de los últimos 6 meses (se agrupa en Python para no
    # depender de funciones de fecha propias de MySQL)
    meses = []
    anio, mes = ahora.year, ahora.month

    for _ in range(6):
        meses.append((anio, mes))
        mes -= 1
        if mes == 0:
            mes, anio = 12, anio - 1

    meses.reverse()
    inicio = datetime(meses[0][0], meses[0][1], 1)

    pedidos_periodo = session.query(Pedido.fecha_pedido, Pedido.total).filter(
        Pedido.estado.in_(ESTADOS_VENTA),
        Pedido.fecha_pedido >= inicio
    ).all()

    acumulado = {m: {"total": 0, "pedidos": 0} for m in meses}

    for fecha, total in pedidos_periodo:
        if fecha and (fecha.year, fecha.month) in acumulado:
            acumulado[(fecha.year, fecha.month)]["total"] += total or 0
            acumulado[(fecha.year, fecha.month)]["pedidos"] += 1

    ventas_por_mes = [
        {
            "mes": f"{MESES[m - 1]} {a}",
            "total": round(acumulado[(a, m)]["total"], 2),
            "pedidos": acumulado[(a, m)]["pedidos"]
        }
        for a, m in meses
    ]

    # ---------------- Productos más vendidos ----------------
    subtotal = func.coalesce(
        DetallePedido.subtotal,
        DetallePedido.cantidad * DetallePedido.precio_unitario
    )

    top = session.query(
        Producto.id_producto,
        Producto.nombre,
        func.sum(DetallePedido.cantidad).label("unidades"),
        func.sum(subtotal).label("ingresos")
    ).join(
        DetallePedido, DetallePedido.id_producto == Producto.id_producto
    ).join(
        Pedido, Pedido.id_pedido == DetallePedido.id_pedido
    ).filter(
        Pedido.estado != "cancelado"
    ).group_by(
        Producto.id_producto, Producto.nombre
    ).order_by(
        func.sum(DetallePedido.cantidad).desc()
    ).limit(5).all()

    top_productos = [
        {
            "id_producto": t.id_producto,
            "nombre": t.nombre,
            "unidades": int(t.unidades or 0),
            "ingresos": round(t.ingresos or 0, 2)
        }
        for t in top
    ]

    # ---------------- Productos por categoría ----------------
    por_categoria = session.query(
        Categoria.nombre,
        func.count(Producto.id_producto)
    ).outerjoin(
        Producto, Producto.id_categoria == Categoria.id_categoria
    ).group_by(
        Categoria.id_categoria, Categoria.nombre
    ).order_by(
        func.count(Producto.id_producto).desc()
    ).all()

    productos_por_categoria = [
        {"categoria": nombre, "cantidad": cantidad}
        for nombre, cantidad in por_categoria
    ]

    # ---------------- Alertas de stock bajo ----------------
    umbral = obtener_valor("umbral_stock_bajo")

    bajos = session.query(Producto).filter(
        func.coalesce(Producto.stock, 0) <= umbral
    ).order_by(
        func.coalesce(Producto.stock, 0).asc()
    ).limit(10).all()

    stock_bajo = [
        {
            "id_producto": p.id_producto,
            "nombre": p.nombre,
            "stock": p.stock or 0
        }
        for p in bajos
    ]

    # ---------------- Últimos pedidos ----------------
    ultimos = session.query(Pedido, Usuario).outerjoin(
        Usuario, Usuario.id_usuario == Pedido.id_usuario
    ).order_by(
        Pedido.fecha_pedido.desc()
    ).limit(6).all()

    ultimos_pedidos = [
        {
            "id_pedido": pedido.id_pedido,
            "cliente": f"{usuario.nombre} {usuario.apellido or ''}".strip() if usuario else "—",
            "fecha": _fecha_texto(pedido.fecha_pedido),
            "estado": pedido.estado,
            "total": pedido.total or 0
        }
        for pedido, usuario in ultimos
    ]

    return {
        "resumen": {
            "ingresos": round(ingresos, 2),
            "total_pedidos": total_pedidos,
            "pedidos_vendidos": pedidos_vendidos,
            "ticket_promedio": round(ticket_promedio, 2),
            "total_usuarios": total_usuarios,
            "total_clientes": total_usuarios - total_admins,
            "total_admins": total_admins,
            "nuevos_usuarios_30d": nuevos_usuarios_30d,
            "total_productos": total_productos,
            "productos_activos": productos_activos,
            "sin_stock": sin_stock,
            "valor_inventario": round(valor_inventario, 2)
        },
        "umbral_stock_bajo": umbral,
        "pedidos_por_estado": pedidos_por_estado,
        "ventas_por_mes": ventas_por_mes,
        "top_productos": top_productos,
        "productos_por_categoria": productos_por_categoria,
        "stock_bajo": stock_bajo,
        "ultimos_pedidos": ultimos_pedidos,
        "generado": _fecha_texto(ahora)
    }


# =========================================================
# USUARIOS Y ROLES
# =========================================================

@admin_bp.route("/usuarios", methods=["GET"])
@token_required
@rol_required("admin")
def listar_usuarios():

    try:
        usuarios = session.query(Usuario).order_by(
            Usuario.fecha_registro.desc()
        ).all()

    except SQLAlchemyError:
        session.rollback()
        return jsonify({"error": "No se pudieron consultar los usuarios"}), 500

    return jsonify([
        {
            "id_usuario": u.id_usuario,
            "nombre": u.nombre,
            "apellido": u.apellido,
            "email": u.email,
            "rol": u.rol,
            "fecha_registro": _fecha_texto(u.fecha_registro)
        }
        for u in usuarios
    ]), 200


@admin_bp.route("/usuarios/<int:id_usuario>/rol", methods=["PUT"])
@token_required
@rol_required("admin")
def cambiar_rol(id_usuario):

    data = request.get_json(silent=True) or {}
    nuevo_rol = data.get("rol")

    if nuevo_rol not in ("cliente", "admin"):
        return jsonify({"error": "El rol debe ser 'cliente' o 'admin'"}), 400

    if id_usuario == request.usuario.id_usuario:
        return jsonify({"error": "No puedes cambiar tu propio rol"}), 400

    try:
        usuario = session.query(Usuario).filter(
            Usuario.id_usuario == id_usuario
        ).first()

        if not usuario:
            return jsonify({"error": "Usuario no encontrado"}), 404

        usuario.rol = nuevo_rol
        session.commit()

    except SQLAlchemyError:
        session.rollback()
        return jsonify({"error": "No se pudo actualizar el rol"}), 500

    return jsonify({
        "message": f"{usuario.nombre} ahora es {nuevo_rol}",
        "id_usuario": usuario.id_usuario,
        "rol": usuario.rol
    }), 200
