from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, Boolean, DateTime, Enum, func
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

from src.models import Base

class Pago(Base): 
    __tablename__="pagos" 
    
    id_pago=Column( Integer, primary_key=True ) 
    metodo_pago=Column( Enum( "tarjeta", "transferencia", "contraentrega" ) ) 
    monto=Column(Float) 
    estado=Column( Enum( "pendiente", "aprobado", "rechazado" ) ) 
    fecha_pago=Column( DateTime, default=func.now() ) 
    id_pedido=Column( Integer, ForeignKey( "pedidos.id_pedido" ) ) 
    pedido=relationship( "Pedido", back_populates="pagos" )