from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, Boolean, DateTime, Enum, func
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

from src.models import Base

class MovimientoInventario(Base):

    __tablename__="movimientos_inventario" 
    
    id_movimiento=Column( Integer, primary_key=True ) 
    tipo=Column( Enum( "entrada", "salida" ) ) 
    cantidad=Column(Integer) 
    descripcion=Column(Text) 
    fecha=Column( DateTime, default=func.now() ) 
    id_producto=Column( Integer, ForeignKey( "productos.id_producto" ) )