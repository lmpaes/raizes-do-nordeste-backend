from fastapi import APIRouter

from app.application.services.pedido_service import PedidoService

router = APIRouter()

@router.post("/pedidos")
def criar_pedido():
    service = PedidoService()

    pedido = service.criar_pedido(
        usuario_id=1,
        unidade_id=1,
        canal_pedido="APP",
        itens=[
            {"produto_id": 1, "quantidade": 2}
        ]
    )

    return {"pedido_id": pedido.id}