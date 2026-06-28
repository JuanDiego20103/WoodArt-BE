from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

from src.models import Base

class Direccion(Base): 
    __tablename__ = "direcciones" 

    id_direccion = Column( Integer, primary_key=True ) 
    direccion = Column(String(255)) 
    ciudad = Column(String(100)) 
    departamento = Column(String(100)) 
    codigo_postal = Column(String(20)) 
    pais = Column(String(100)) 
    id_usuario = Column( Integer, ForeignKey( "usuarios.id_usuario" ) ) 
    usuario = relationship( "Usuario", back_populates="direcciones" )