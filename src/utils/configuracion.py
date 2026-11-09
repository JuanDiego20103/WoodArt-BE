import json

from src.models import session
from src.models.configuracion import Configuracion


# =========================================================
# CONFIGURACIONES DISPONIBLES Y SUS VALORES POR DEFECTO
# =========================================================
# Solo estas claves se pueden leer y modificar desde el panel.

CONFIGURACION_DEFECTO = {

    "nombre_tienda": {
        "valor": "WoodArt",
        "tipo": "texto",
        "etiqueta": "Nombre de la tienda",
        "descripcion": "Se muestra en el encabezado de la tienda.",
        "publica": True
    },

    "mensaje_oferta": {
        "valor": "🔥 20% de descuento en muebles seleccionados",
        "tipo": "texto",
        "etiqueta": "Mensaje de ofertas",
        "descripcion": "Texto del banner de ofertas en la página de inicio.",
        "publica": True
    },

    "umbral_stock_bajo": {
        "valor": 5,
        "tipo": "entero",
        "etiqueta": "Umbral de stock bajo",
        "descripcion": "Los productos con este stock o menos aparecen como alerta en las analíticas.",
        "publica": False
    },

    "registro_abierto": {
        "valor": True,
        "tipo": "booleano",
        "etiqueta": "Permitir registro de clientes",
        "descripcion": "Si se desactiva, nadie puede crear cuentas nuevas desde la tienda.",
        "publica": True
    },

    "modo_mantenimiento": {
        "valor": False,
        "tipo": "booleano",
        "etiqueta": "Modo mantenimiento",
        "descripcion": "Cierra la tienda para los clientes. Los administradores pueden seguir entrando.",
        "publica": True
    },

    "mensaje_mantenimiento": {
        "valor": "Estamos haciendo mejoras en la tienda. Vuelve pronto.",
        "tipo": "texto",
        "etiqueta": "Mensaje de mantenimiento",
        "descripcion": "Lo que ven los clientes mientras la tienda está en mantenimiento.",
        "publica": True
    },
}


# =========================================================
# LEER CONFIGURACIÓN
# =========================================================

def obtener_configuracion(solo_publica=False):
    """
    Devuelve un diccionario {clave: valor} con los valores guardados
    en la base de datos o, si no existen, los valores por defecto.
    """

    guardadas = {
        c.clave: c.valor
        for c in session.query(Configuracion).all()
    }

    configuracion = {}

    for clave, info in CONFIGURACION_DEFECTO.items():

        if solo_publica and not info["publica"]:
            continue

        valor = info["valor"]

        if clave in guardadas:
            try:
                valor = json.loads(guardadas[clave])
            except (TypeError, ValueError):
                pass

        configuracion[clave] = valor

    return configuracion


def obtener_valor(clave):
    return obtener_configuracion().get(clave)


# =========================================================
# VALIDAR Y GUARDAR CONFIGURACIÓN
# =========================================================

def validar_valor(clave, valor):
    """
    Convierte y valida el valor según su tipo.
    Devuelve (valor_convertido, error).
    """

    info = CONFIGURACION_DEFECTO.get(clave)

    if not info:
        return None, f"La configuración '{clave}' no existe"

    tipo = info["tipo"]

    if tipo == "booleano":

        if isinstance(valor, bool):
            return valor, None

        if isinstance(valor, str) and valor.lower() in ("true", "1", "si", "sí", "on"):
            return True, None

        if isinstance(valor, str) and valor.lower() in ("false", "0", "no", "off", ""):
            return False, None

        return None, f"'{info['etiqueta']}' debe ser verdadero o falso"

    if tipo == "entero":

        try:
            numero = int(valor)
        except (TypeError, ValueError):
            return None, f"'{info['etiqueta']}' debe ser un número entero"

        if numero < 0:
            return None, f"'{info['etiqueta']}' no puede ser negativo"

        return numero, None

    # texto
    texto = str(valor or "").strip()

    if len(texto) > 255:
        return None, f"'{info['etiqueta']}' no puede tener más de 255 caracteres"

    if clave == "nombre_tienda" and not texto:
        return None, "El nombre de la tienda no puede estar vacío"

    return texto, None


def guardar_configuracion(cambios):
    """
    Guarda un diccionario {clave: valor}. Devuelve (configuracion, errores).
    No guarda nada si algún valor es inválido.
    """

    errores = []
    validados = {}

    for clave, valor in cambios.items():

        convertido, error = validar_valor(clave, valor)

        if error:
            errores.append(error)
        else:
            validados[clave] = convertido

    if errores:
        return None, errores

    for clave, valor in validados.items():

        fila = session.query(Configuracion).filter(
            Configuracion.clave == clave
        ).first()

        # ensure_ascii evita problemas con emojis en tablas que no son utf8mb4
        valor_json = json.dumps(valor)

        if fila:
            fila.valor = valor_json
        else:
            session.add(Configuracion(clave=clave, valor=valor_json))

    session.commit()

    return obtener_configuracion(), []
