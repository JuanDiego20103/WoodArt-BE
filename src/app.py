from flask import Flask
from src.models import Base, engine
from src.models.usuarios import Usuario
from src.models.direcciones import Direccion
from src.models.categorias import Categoria
from src.models.productos import Producto
from src.models.imagen_productos import ImagenProducto
from src.models.pedidos import Pedido
from src.models.detalle_pedido import DetallePedido
from src.models.pagos import Pago
from src.models.carrito import Carrito
from src.models.inventario import MovimientoInventario
from src.routes import all_blueprints

app=Flask(__name__)

Base.metadata.create_all(engine)

prefix="/api/v1"
for bp in all_blueprints:
    print(bp)
    url_prefix=f"{prefix}/{bp.name}"
    print(url_prefix)
    app.register_blueprint(bp, url_prefix=url_prefix)



if __name__=="__main__":

    print(app.url_map)

    app.run(debug=True)
