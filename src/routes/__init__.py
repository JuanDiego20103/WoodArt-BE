from .usuarios_routes import usuarios_bp
from .productos_routes import productos_bp
from .pedidos_routes import pedidos_bp
from .carrito_routes import carrito_bp
from .categorias_routes import categorias_bp
from .direcciones_routes import direcciones_bp
from .pagos_routes import pagos_bp
from .inventario_routes import inventario_bp
from .imagen_producto_routes import imagen_producto_bp
from .detalle_pedido_routes import detalle_pedido_bp
from .admin_routes import admin_bp
from .configuracion_routes import configuracion_bp

all_blueprints = [usuarios_bp, productos_bp, pedidos_bp, carrito_bp, categorias_bp, direcciones_bp, pagos_bp, inventario_bp, imagen_producto_bp, detalle_pedido_bp, admin_bp, configuracion_bp]
