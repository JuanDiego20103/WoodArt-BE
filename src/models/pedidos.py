from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, Boolean, DateTime, Enum, func
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

from src.models import Base

class Pedido(Base): 
    __tablename__="pedidos" 
    id_pedido=Column( Integer, primary_key=True ) 
    fecha_pedido=Column( DateTime, default=func.now() ) 
    estado=Column( Enum( "pendiente", "pagado", "enviado", "entregado", "cancelado" ), default="pendiente" ) 
    total=Column(Float) 
    id_usuario=Column( Integer, ForeignKey( "usuarios.id_usuario" ) ) 
    usuario=relationship( "Usuario", back_populates="pedidos" ) 
    detalles=relationship( "DetallePedido", back_populates="pedido" ) 
    pagos=relationship( "Pago", back_populates="pedido" )