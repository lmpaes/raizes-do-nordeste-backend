from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, Enum, String
from datetime import datetime
import enum
from app.core.database import Base


# Define os possíveis resultados do processamento de pagamento
class StatusPagamento(enum.Enum):
    APROVADO = "aprovado"
    RECUSADO = "recusado"


# Registra as informações do pagamento associado a um pedido
class Pagamento(Base):
    __tablename__ = "pagamentos"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    status = Column(Enum(StatusPagamento), nullable=False)
    valor = Column(Float, nullable=False)
    metodo = Column(String, default="mock")
    data_pagamento = Column(DateTime, default=datetime.utcnow)