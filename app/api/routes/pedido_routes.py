# Rotas de pedido responsáveis por receber a requisição autenticada do cliente
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.application.services.pedido_service import PedidoService
from app.core.security import require_roles
from app.core.database import get_db
from app.api.schemas.pedido_schema import PedidoCreate
from app.infrastructure.models.usuario_model import Usuario

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


@router.post("/")
def criar_pedido(
    request: PedidoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles("CLIENTE", "ADMIN"))
):
    # Instancia o serviço que concentra o fluxo de criação do pedido
    service = PedidoService()

    # Cria o pedido usando o usuário autenticado obtido pelo token
    pedido = service.criar_pedido(
        db=db,
        dados_pedido=request,
        usuario_id=current_user.id
    )

    # Retorna os dados principais do pedido para o cliente
    return {
        "id": pedido.id,
        "status": pedido.status,
        "total": pedido.valor_total,
        "pontos_gerados": getattr(pedido, "pontos_gerados", 0)
    }
