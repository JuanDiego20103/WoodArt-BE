from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, Boolean, DateTime, Enum
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

from src.models import Base

class Categoria(Base): 

    __tablename__="categorias" 
    
    id_categoria=Column( Integer, primary_key=True ) 
    nombre=Column( String(100), nullable=False ) 
    descripcion=Column(Text) 
    productos=relationship( "Producto", back_populates="categoria" )