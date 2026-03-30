from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, Enum
from datetime import datetime
import enum

from app.core.database import Base


class StatusPedido(enum.Enum):
    CRIADO = "criado"
    AGUARDANDO_PAGAMENTO = "aguardando_pagamento"
    PAGO = "pago"
    CANCELADO = "cancelado"
    FINALIZADO = "finalizado"


class CanalPedido(enum.Enum):
    APP = "app"
    WEB = "web"
    BALCAO = "balcao"
    TOTEM = "totem"


class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    unidade_id = Column(Integer, ForeignKey("unidades.id"), nullable=False)
    status = Column(Enum(StatusPedido), default=StatusPedido.CRIADO)
    canal_pedido = Column(Enum(CanalPedido), nullable=False)
    valor_total = Column(Float, default=0)
    data_criacao = Column(DateTime, default=datetime.utcnow)