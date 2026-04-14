# Rotas responsáveis pelo cadastro e gerenciamento de usuários do sistema
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.api.schemas.usuario_schema import UsuarioCreate, UsuarioResponse
from app.application.services.usuario_service import UsuarioService

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


# Cria e finaliza a conexão com o banco de dados a cada requisição
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=UsuarioResponse)
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    try:
        # Envia os dados para a camada de serviço, onde são aplicadas as regras de negócio
        return UsuarioService.criar_usuario(db, usuario)
    except ValueError as e:
        # Retorna erro de validação caso alguma regra não seja atendida
        raise HTTPException(status_code=400, detail=str(e))