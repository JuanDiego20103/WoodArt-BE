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
from src.models.configuracion import Configuracion
from src.routes import all_blueprints
from src.models import session
import os
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app=Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

# Orígenes permitidos del frontend (ionic serve = 8100, ng serve/npm start = 4200).
CORS_ORIGINS = [
    "http://localhost:8100",
    "http://127.0.0.1:8100",
    "http://localhost:4200",
    "http://127.0.0.1:4200",
]
# En producción se agregan los dominios del frontend desplegado,
# separados por comas, en la variable CORS_ORIGINS.
CORS_ORIGINS += [o.strip() for o in os.getenv("CORS_ORIGINS", "").split(",") if o.strip()]
CORS(app, resources={r"/api/*": {"origins": CORS_ORIGINS}})

Base.metadata.create_all(engine)


# Cierra la sesión de la base de datos al terminar cada petición.
# Sin esto, la sesión global mantiene abierta una transacción y no ve
# cambios hechos desde fuera (por ejemplo, un rol cambiado con crear_admin.py).
@app.teardown_appcontext
def cerrar_sesion_bd(exception=None):
    session.close()

# Ruta de verificación: Render y los navegadores pueden comprobar que la API responde.
@app.route("/")
def estado():
    return {"servicio": "WoodArt API", "estado": "ok", "api": "/api/v1"}


prefix="/api/v1"
for bp in all_blueprints:
    print(bp)
    url_prefix=f"{prefix}/{bp.name}"
    print(url_prefix)
    app.register_blueprint(bp, url_prefix=url_prefix)



if __name__=="__main__":
    print(app.url_map)

    app.run(debug=True)
