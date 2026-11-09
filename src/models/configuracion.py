from sqlalchemy import Column, String, Text, DateTime, func

from src.models import Base


class Configuracion(Base):
    """
    Configuración general del sistema (clave / valor).

    Los valores se guardan como JSON en texto para poder
    almacenar números, booleanos y textos en la misma tabla.
    """

    __tablename__ = "configuracion"

    clave = Column(String(100), primary_key=True)
    valor = Column(Text)
    fecha_actualizacion = Column(
        DateTime,
        default=func.now(),
        onupdate=func.now()
    )

    def __repr__(self):
        return f"<Configuracion(clave='{self.clave}', valor='{self.valor}')>"
