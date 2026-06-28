from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, Boolean, DateTime, Enum
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

from src.models import Base

class Carrito(Base): 
    
    __tablename__="carrito" 
    id_carrito=Column( Integer, primary_key=True ) 
    cantidad=Column(Integer) 
    id_usuario=Column( Integer, ForeignKey( "usuarios.id_usuario" ) ) 
    id_producto=Column( Integer, ForeignKey( "productos.id_producto" ) )