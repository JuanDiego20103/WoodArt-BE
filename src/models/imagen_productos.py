from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, Boolean, DateTime, Enum
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

from src.models import Base

class ImagenProducto(Base): 
    __tablename__="imagenes_producto" 
    id_imagen=Column( Integer, primary_key=True ) 
    ruta_imagen=Column( String(255) ) 
    id_producto=Column( Integer, ForeignKey( "productos.id_producto" ) ) 
    producto=relationship( "Producto", back_populates="imagenes" )