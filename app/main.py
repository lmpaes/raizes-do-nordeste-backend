# Arquivo principal responsável por iniciar a aplicação FastAPI
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.routes import estoque_routes, pedido_routes, produto_routes, unidade_routes
from app.api.routes.auth_routes import router as auth_router
from app.api.routes.usuario_routes import router as usuario_router
from app.core.database import Base, engine
from app.domain.exceptions import DomainException, formatar_erro
from app.infrastructure.models.estoque_model import Estoque
from app.infrastructure.models.fidelidade_model import Fidelidade
from app.infrastructure.models.item_pedido_model import ItemPedido
from app.infrastructure.models.pagamento_model import Pagamento
from app.infrastructure.models.pedido_model import Pedido
from app.infrastructure.models.produto_model import Produto
from app.infrastructure.models.unidade_model import Unidade
from app.infrastructure.models.usuario_model import Usuario


app = FastAPI(title="Raízes do Nordeste API")


# Trata de forma centralizada as exceções de domínio da aplicação
@app.exception_handler(DomainException)
async def domain_exception_handler(request: Request, exc: DomainException):
    return JSONResponse(
        status_code=exc.status_code,
        content=formatar_erro(exc, str(request.url.path))
    )


# Cria as tabelas mapeadas no banco ao iniciar a aplicação
Base.metadata.create_all(bind=engine)

# Registra os módulos de rota disponíveis na API
app.include_router(usuario_router)
app.include_router(auth_router)
app.include_router(pedido_routes.router)
app.include_router(unidade_routes.router)
app.include_router(produto_routes.router)
app.include_router(estoque_routes.router)


@app.get("/")
def root():
    # Endpoint simples para verificar se a API está ativa
    return {"message": "API funcionando corretamente"}
