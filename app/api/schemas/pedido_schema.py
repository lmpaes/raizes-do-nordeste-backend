# Schemas responsáveis por validar os dados de entrada do pedido
from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class CanalPedidoEnum(str, Enum):
    APP = "APP"
    TOTEM = "TOTEM"
    BALCAO = "BALCAO"
    PICKUP = "PICKUP"
    WEB = "WEB"

    # Dados necessários para incluir um produto no pedido
class ItemPedidoCreate(BaseModel):
    produto_id: int = Field(..., example=1)
    quantidade: int = Field(..., gt=0, example=2)

    # Dados principais necessários para criar um pedido
class PedidoCreate(BaseModel):

    unidade_id: int = Field(..., example=1)
    canal_pedido: CanalPedidoEnum
    itens: List[ItemPedidoCreate]
