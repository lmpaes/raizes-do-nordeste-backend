from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, Enum
from datetime import datetime
import enum

from app.core.database import Base


class StatusPedido(enum.Enum):
    AGUARDANDO_PAGAMENTO = "AGUARDANDO_PAGAMENTO"
    PAGO = "PAGO"
    RECUSADO = "RECUSADO"
    CANCELADO = "CANCELADO"
    FINALIZADO = "FINALIZADO"


class CanalPedido(enum.Enum):
    APP = "APP"
    WEB = "WEB"
    BALCAO = "BALCAO"
    TOTEM = "TOTEM"


class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    unidade_id = Column(Integer, ForeignKey("unidades.id"), nullable=False)
    status = Column(Enum(StatusPedido), default=StatusPedido.AGUARDANDO_PAGAMENTO)
    canal_pedido = Column(Enum(CanalPedido), nullable=False)
    valor_total = Column(Float, default=0)
    data_criacao = Column(DateTime, default=datetime.utcnow)