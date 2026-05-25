# Rotas de estoque responsáveis por cadastrar ou somar produtos em estoque
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.infrastructure.models.estoque_model import Estoque
from app.infrastructure.models.produto_model import Produto
from app.infrastructure.models.unidade_model import Unidade
from app.api.schemas.estoque_schema import EstoqueCreate

router = APIRouter(prefix="/estoque", tags=["Estoque"])


# Abre e fecha a sessão com o banco a cada requisição
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def criar_estoque(data: EstoqueCreate, db: Session = Depends(get_db)):

    # Verifica se o produto existe
    produto = db.query(Produto).filter(Produto.id == data.produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="PRODUTO_NAO_ENCONTRADO")

    # Verifica se a unidade existe
    unidade = db.query(Unidade).filter(Unidade.id == data.unidade_id).first()
    if not unidade:
        raise HTTPException(status_code=404, detail="UNIDADE_NAO_ENCONTRADA")

    # Garante que o produto pertence à unidade informada
    if produto.unidade_id != data.unidade_id:
        raise HTTPException(
            status_code=400,
            detail="PRODUTO_NAO_PERTENCE_A_UNIDADE"
        )

    # Verifica se já existe estoque cadastrado para o produto na unidade
    estoque = db.query(Estoque).filter(
        Estoque.produto_id == data.produto_id,
        Estoque.unidade_id == data.unidade_id
    ).first()

    # Soma a quantidade ao estoque atual quando já existir registro
    if estoque:
        estoque.quantidade += data.quantidade
    else:
        # Cria um novo registro quando for a primeira entrada no estoque
        estoque = Estoque(
            produto_id=data.produto_id,
            unidade_id=data.unidade_id,
            quantidade=data.quantidade
        )

    # Salva o estoque atualizado no banco
    db.add(estoque)
    db.commit()
    db.refresh(estoque)

    return estoque
