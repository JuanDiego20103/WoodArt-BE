# WoodArt — Backend (API REST)

API REST de **WoodArt**, una tienda en línea de productos en madera (maderas, muebles, herrajes, pisos y puertas). Guarda y entrega los datos en formato JSON y es la única parte del sistema que se conecta a la base de datos. La tienda que ve el usuario está en el proyecto **WoodArt** (frontend), que consume esta API.

Proyecto del programa **Análisis y Desarrollo de Software (ADSO)** — ficha 3186693.

## Tecnologías

| Tecnología | Uso |
| --- | --- |
| Python + Flask 3 | Servidor de la API y rutas organizadas en *blueprints* |
| SQLAlchemy 2 + PyMySQL | ORM y conexión con MySQL |
| MySQL (XAMPP) | Base de datos `woodart_PY` |
| PyJWT | Tokens de inicio de sesión (JWT) que vencen en 2 horas |
| Werkzeug | Cifrado (hash) de contraseñas |
| python-dotenv | Lectura de la clave secreta desde `.env` |

## Requisitos

- Python 3.12 o superior
- XAMPP con **MySQL** encendido en el puerto 3306 (usuario `root` sin contraseña)
- Una base de datos vacía llamada `woodart_PY`. Créala en phpMyAdmin o con:

```sql
CREATE DATABASE woodart_PY CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
```

Las tablas se crean solas la primera vez que arranca la API.

## Instalación

```bash
# 1. Crear y activar el entorno virtual (Windows)
python -m venv .venv
.venv\Scripts\activate

# 2. Instalar las dependencias
pip install flask sqlalchemy pymysql pyjwt python-dotenv
```

3. Crea el archivo `src/.env` con la clave para firmar los tokens. Usa una clave larga y propia; este archivo **no se sube al repositorio**.

```env
JWT_SECRET_KEY=escribe-aqui-una-clave-larga-y-secreta
```

## Ejecución

Con doble clic en **`iniciar_backend.bat`**, o desde la carpeta `WoodArt_backend`:

```bash
.venv\Scripts\python.exe -m src.app
```

La API queda disponible en **http://127.0.0.1:5000/api/v1**. Arranca el backend **antes** que el frontend.

### Crear el primer administrador

Las cuentas que se registran desde la tienda siempre quedan como *cliente*. Para crear un administrador, o convertir una cuenta existente en administrador o cambiarle la contraseña, haz doble clic en **`crear_admin.bat`** y sigue las instrucciones. Al final el script verifica que el acceso funcione.

## Estructura

```
WoodArt_backend/
├── crear_admin.py          # Crea o promueve administradores
├── crear_admin.bat
├── iniciar_backend.bat
└── src/
    ├── app.py              # Punto de entrada: crea la app, las tablas y registra las rutas
    ├── .env                # Clave secreta (no se versiona)
    ├── models/             # Tablas como clases de SQLAlchemy
    │   ├── __init__.py     # Conexión a MySQL y sesión
    │   ├── usuarios.py, productos.py, categorias.py, carrito.py,
    │   ├── pedidos.py, detalle_pedido.py, pagos.py, direcciones.py,
    │   └── imagen_productos.py, inventario.py, configuracion.py
    ├── routes/             # Endpoints de la API (un blueprint por recurso)
    └── utils/
        ├── auth.py         # Decoradores token_required y rol_required
        └── configuracion.py# Valores y validación de la configuración de la tienda
```

## Autenticación

1. `POST /api/v1/usuarios/login` con `email` y `password` devuelve un `access_token`.
2. Las rutas protegidas reciben el token en el encabezado:

```
Authorization: Bearer <access_token>
```

- Sin token, o con un token vencido o inválido, la API responde **401**.
- Si la ruta es solo para administradores y el usuario es cliente, la API responde **403**.

## Endpoints principales

Todas las rutas empiezan por `/api/v1`.

| Método | Ruta | Acceso | Descripción |
| --- | --- | --- | --- |
| POST | `/usuarios` | Público | Registrar un cliente (si el registro está abierto) |
| POST | `/usuarios/login` | Público | Iniciar sesión y recibir el token JWT |
| GET | `/usuarios/perfil` | Token | Datos del usuario del token |
| GET | `/usuarios/` | Admin | Listar usuarios |
| GET | `/productos` | Público | Listar productos. Parámetros: `page`, `per_page`, `id_categoria`, `q` (búsqueda) |
| GET | `/productos/<id>` | Público | Ver un producto |
| POST | `/productos` | Admin | Crear un producto |
| PUT | `/productos/<id>` | Admin | Editar un producto |
| DELETE | `/productos/<id>` | Admin | Eliminar un producto |
| GET | `/categorias/` | Público | Listar categorías |
| POST | `/carrito` | Token | Agregar un producto (si ya está, suma la cantidad) |
| GET | `/carrito?id_usuario=<id>` | Token | Ver el carrito con subtotales |
| DELETE | `/carrito/<id_carrito>` | Token | Quitar un producto del carrito propio |
| GET | `/admin/estadisticas` | Admin | Analíticas: ingresos, pedidos, ventas por mes, más vendidos, stock bajo |
| GET | `/admin/usuarios` | Admin | Usuarios con su rol y fecha de registro |
| PUT | `/admin/usuarios/<id>/rol` | Admin | Cambiar el rol entre `cliente` y `admin` |
| GET | `/configuracion/publica` | Público | Configuración que usa la tienda |
| GET / PUT | `/configuracion` | Admin | Ver y cambiar la configuración de la tienda |

Las rutas de pedidos, pagos, direcciones, imágenes e inventario existen pero **siguen en desarrollo**.

## Autor

Juan Diego Bulla Rodríguez — ADSO, ficha 3186693.

## Licencia

MIT. Consulta el archivo [LICENSE](LICENSE).
