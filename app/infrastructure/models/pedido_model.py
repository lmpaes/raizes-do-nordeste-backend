from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, Enum
from datetime import datetime
import enum

from app.core.database import Base


# Define os possíveis status de um pedido ao longo do seu ciclo
class StatusPedido(enum.Enum):
    AGUARDANDO_PAGAMENTO = "AGUARDANDO_PAGAMENTO"
    PAGO = "PAGO"
    RECUSADO = "RECUSADO"
    CANCELADO = "CANCELADO"
    FINALIZADO = "FINALIZADO"


# Representa os canais pelos quais o pedido pode ser realizado (APP, WEB, BALCAO, TOTEM)
class CanalPedido(enum.Enum):
    APP = "APP"
    WEB = "WEB"
    BALCAO = "BALCAO"
    TOTEM = "TOTEM"


# Modelo principal do sistema, responsável por armazenar os dados do pedido
class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    unidade_id = Column(Integer, ForeignKey("unidades.id"), nullable=False)
    status = Column(Enum(StatusPedido), default=StatusPedido.AGUARDANDO_PAGAMENTO)
    canal_pedido = Column(Enum(CanalPedido), nullable=False)
    valor_total = Column(Float, default=0)
    data_criacao = Column(DateTime, default=datetime.utcnow)