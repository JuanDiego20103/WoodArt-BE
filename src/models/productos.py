from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, Boolean, DateTime, Enum, func
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

from src.models import Base

class Producto(Base): 
    __tablename__="productos" 

    id_producto=Column( Integer, primary_key=True ) 
    nombre=Column( String(200), nullable=False ) 
    descripcion=Column(Text) 
    precio=Column( Float, nullable=False ) 
    stock=Column( Integer, default=0 ) 
    material=Column( String(100) ) 
    color=Column( String(100) )  
    imagen_principal=Column( String(255) ) 
    dimensiones=Column( String(100) )
    peso=Column( Float )
    activo=Column( Boolean, default=True ) 
    fecha_creacion=Column( DateTime, default=func.now() ) 
    id_categoria=Column( Integer, ForeignKey( "categorias.id_categoria" ) ) 
    categoria=relationship( "Categoria", back_populates="productos" ) 
    imagenes=relationship( "ImagenProducto", back_populates="producto" )