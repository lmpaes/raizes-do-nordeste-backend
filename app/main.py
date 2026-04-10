from fastapi import FastAPI

from app.api.routes.usuario_routes import router as usuario_router
from app.api.routes.auth_routes import router as auth_router
from app.api.routes import pedido_routes

from app.core.database import Base, engine

from app.infrastructure.models.usuario_model import Usuario
from app.infrastructure.models.unidade_model import Unidade
from app.infrastructure.models.produto_model import Produto
from app.infrastructure.models.estoque_model import Estoque
from app.infrastructure.models.pedido_model import Pedido
from app.infrastructure.models.item_pedido_model import ItemPedido
from app.infrastructure.models.pagamento_model import Pagamento
from app.infrastructure.models.fidelidade_model import Fidelidade


app = FastAPI(title="Raízes do Nordeste API")

Base.metadata.create_all(bind=engine)

app.include_router(usuario_router)
app.include_router(auth_router)
app.include_router(pedido_routes.router)


@app.get("/")
def root():
    return {"message": "API funcionando corretamente"}