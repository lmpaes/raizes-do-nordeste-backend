from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List

from app.application.services.pedido_service import PedidoService
from app.core.security import get_current_user

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


class ItemPedidoRequest(BaseModel):
    produto_id: int
    quantidade: int


class PedidoRequest(BaseModel):
    usuario_id: int
    unidade_id: int
    canal_pedido: str
    itens: List[ItemPedidoRequest]


@router.post("/")
def criar_pedido(
    request: PedidoRequest,
    current_user = Depends(get_current_user)
):
    service = PedidoService()

    pedido = service.criar_pedido(
        usuario_id=request.usuario_id,
        unidade_id=request.unidade_id,
        canal_pedido=request.canal_pedido,
        itens=[item.dict() for item in request.itens]
    )

    return {
        "id": pedido.id,
        "status": pedido.status.value,
        "valor_total": pedido.valor_total
    }