from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.infrastructure.models.unidade_model import Unidade
from app.api.schemas.unidade_schema import UnidadeCreate

router = APIRouter(prefix="/unidades", tags=["Unidades"])


# Controla a sessão com o banco a cada requisição
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def criar_unidade(data: UnidadeCreate, db: Session = Depends(get_db)):

    # Cria uma nova unidade da rede
    unidade = Unidade(
        nome=data.nome,
        cidade=data.cidade,
        estado=data.estado
    )

    db.add(unidade)
    db.commit()
    db.refresh(unidade)

    return unidade