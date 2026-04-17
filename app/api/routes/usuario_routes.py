# Rotas responsáveis pelo cadastro e gerenciamento de usuários
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.api.schemas.usuario_schema import UsuarioCreate, UsuarioResponse
from app.application.services.usuario_service import UsuarioService

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


# Controla a sessão com o banco a cada requisição
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=UsuarioResponse)
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    try:
        # Envia os dados para o service (validações e regras de negócio)
        return UsuarioService.criar_usuario(db, usuario)
    except ValueError as e:
        # Retorna erro caso alguma regra não seja atendida
        raise HTTPException(status_code=400, detail=str(e))