from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, Boolean, DateTime, Enum
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

from src.models import Base

class DetallePedido(Base):

    __tablename__="detalle_pedido"
     
    id_detalle=Column( Integer, primary_key=True ) 
    cantidad=Column(Integer) 
    precio_unitario=Column(Float) 
    subtotal=Column(Float) 
    id_pedido=Column( Integer, ForeignKey( "pedidos.id_pedido" ) ) 
    id_producto=Column( Integer, ForeignKey( "productos.id_producto" ) ) 
    pedido=relationship( "Pedido", back_populates="detalles" )