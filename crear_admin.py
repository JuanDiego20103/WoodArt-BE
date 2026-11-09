"""
Crea un usuario administrador para WoodArt, convierte en administrador
a un usuario que ya existe o le cambia la contraseña.

Uso (desde la carpeta WoodArt_backend):
    .venv\\Scripts\\python.exe crear_admin.py
o con doble clic en crear_admin.bat
"""

from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash

from src.models import Base, engine, session
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


def pedir(texto, obligatorio=True):
    while True:
        valor = input(texto).strip()
        if valor or not obligatorio:
            return valor
        print("  Este campo es obligatorio.")


def pedir_password():
    """
    La contraseña se escribe de forma visible a propósito: es un script
    de desarrollo y así se evitan errores al teclear o pegar.
    """
    print("\n(La contraseña se verá en pantalla. Escríbela, no la pegues.)")

    while True:
        password = input("Contraseña nueva: ")

        if password != password.strip():
            print("  La contraseña no puede empezar ni terminar con espacios.")
            continue

        if len(password) < 6:
            print("  La contraseña debe tener al menos 6 caracteres.")
            continue

        if password != input("Repite la contraseña: "):
            print("  Las contraseñas no coinciden. Intenta de nuevo.")
            continue

        return password


def resumen(usuario, password):
    # Comprueba que la contraseña guardada funciona antes de terminar
    ok = check_password_hash(usuario.password, password)

    print("\n" + "-" * 50)
    print("  Datos para entrar al panel")
    print("-" * 50)
    print(f"  Correo:     {usuario.email}")
    print(f"  Rol:        {usuario.rol}")
    print(f"  Contraseña: verificada {'OK' if ok else 'CON ERROR'}")
    print("  Panel:      http://localhost:5001/admin/login")
    print("-" * 50)


def main():

    Base.metadata.create_all(engine)

    print("=" * 50)
    print("  WoodArt - Crear administrador")
    print("=" * 50)

    email = pedir("Correo del administrador: ").lower()

    usuario = session.query(Usuario).filter(
        func.lower(Usuario.email) == email
    ).first()

    # ------------------------------------------------------
    # La cuenta ya existe
    # ------------------------------------------------------
    if usuario:

        print(f"\nCuenta encontrada: {usuario.nombre} {usuario.apellido or ''} ({usuario.rol})")
        print("  1) Convertir en administrador")
        print("  2) Cambiar la contraseña (y dejarla como administrador)")
        print("  3) Salir sin cambios")

        opcion = pedir("Elige una opción (1, 2 o 3): ")

        if opcion == "1":

            if usuario.rol == "admin":
                print("\nEsta cuenta ya es administrador.")
                print("Si no puedes entrar, vuelve a ejecutar el script y elige la opción 2.")
                return

            usuario.rol = "admin"
            session.commit()
            print(f"\nListo: {usuario.email} ahora es administrador.")
            print("Entra con la contraseña que ya tenía esa cuenta.")
            return

        if opcion == "2":

            password = pedir_password()
            usuario.password = generate_password_hash(password)
            usuario.rol = "admin"
            session.commit()
            print("\nListo: contraseña actualizada.")
            resumen(usuario, password)
            return

        print("Sin cambios.")
        return

    # ------------------------------------------------------
    # La cuenta no existe: se crea
    # ------------------------------------------------------
    print("\nNo existe una cuenta con ese correo. Vamos a crearla.")

    nombre = pedir("Nombre: ")
    apellido = pedir("Apellido: ")
    telefono = pedir("Teléfono (opcional, Enter para omitir): ", obligatorio=False)
    password = pedir_password()

    usuario = Usuario(
        nombre=nombre,
        apellido=apellido,
        email=email,
        telefono=telefono or None,
        password=generate_password_hash(password),
        rol="admin"
    )

    session.add(usuario)
    session.commit()

    print(f"\nListo: administrador {email} creado.")
    resumen(usuario, password)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("\nOcurrió un error:", e)
        print("Revisa que MySQL esté encendido en XAMPP y vuelve a intentarlo.")
