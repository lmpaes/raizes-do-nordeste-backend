from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.infrastructure.models.produto_model import Produto
from app.infrastructure.models.unidade_model import Unidade
from app.api.schemas.produto_schema import ProdutoCreate

router = APIRouter(prefix="/produtos", tags=["Produtos"])


# Controla a sessão com o banco a cada requisição
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def criar_produto(data: ProdutoCreate, db: Session = Depends(get_db)):

    # Verifica se a unidade informada existe
    unidade = db.query(Unidade).filter(Unidade.id == data.unidade_id).first()

    if not unidade:
        raise HTTPException(status_code=404, detail="UNIDADE_NAO_ENCONTRADA")

    # Cria o produto vinculado à unidade
    produto = Produto(
        nome=data.nome,
        descricao=data.descricao,
        preco=data.preco,
        unidade_id=data.unidade_id
    )

    db.add(produto)
    db.commit()
    db.refresh(produto)

    return produto