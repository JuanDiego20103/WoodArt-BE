from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, Boolean, DateTime, Enum, func
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from src.models import Base

class Usuario(Base): 
    __tablename__ = "usuarios"

    id_usuario = Column( Integer, primary_key=True, autoincrement=True ) 
    nombre = Column(String(100),nullable=False) 
    apellido = Column(String(100)) 
    email = Column( String(150), unique=True, nullable=False ) 
    telefono = Column(String(30))
    password = Column(String(255)) 
    rol = Column( Enum( "cliente", "admin" ), default="cliente" ) 
    fecha_registro = Column( DateTime, default=func.now() ) 
    direcciones = relationship( "Direccion", back_populates="usuario" ) 
    pedidos = relationship( "Pedido", back_populates="usuario" )
    def __repr__(self):
        return f"<Usuario(id_usuario={self.id_usuario}, nombre='{self.nombre}', apellido='{self.apellido}', email='{self.email}', telefono='{self.telefono}', rol='{self.rol}', fecha_registro='{self.fecha_registro}')>"
    