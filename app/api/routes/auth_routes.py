# Rotas responsáveis pelo processo de autenticação de usuários (login)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import hashlib

from app.core.database import SessionLocal
from app.infrastructure.repositories.usuario_repository import UsuarioRepository
from app.core.security import criar_token
from app.api.schemas.auth_schema import LoginRequest  # schema do corpo da requisição

router = APIRouter(prefix="/auth", tags=["Auth"])


# Cria e encerra a conexão com o banco de dados a cada requisição
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):

    # Dados recebidos no body (email e senha)
    email = data.email
    senha = data.senha

    # Busca o usuário pelo e-mail
    usuario = UsuarioRepository.buscar_por_email(db, email)

    # Se não encontrar o usuário, retorna erro de autenticação
    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    # Gera o hash da senha informada para validar
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()

    # Compara a senha informada com a armazenada
    if usuario.senha_hash != senha_hash:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    # Gera o token JWT com dados básicos do usuário
    token = criar_token({
        "sub": usuario.email,
        "perfil": usuario.perfil
    })

    # Retorna o token para uso nas próximas requisições
    return {
        "access_token": token,
        "token_type": "bearer"
    }