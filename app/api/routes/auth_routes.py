# Rotas de autenticação responsáveis pelo login e geração do token JWT
import hashlib

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.schemas.auth_schema import LoginRequest
from app.core.database import get_db
from app.core.security import criar_token
from app.infrastructure.repositories.usuario_repository import UsuarioRepository

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    # Busca o usuário pelo e-mail informado no login
    usuario = UsuarioRepository.buscar_por_email(db, data.email)

    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciais invalidas")

    # Gera o hash da senha recebida para comparar com a senha salva
    senha_hash = hashlib.sha256(data.senha.encode()).hexdigest()

    if usuario.senha_hash != senha_hash:
        raise HTTPException(status_code=401, detail="Credenciais invalidas")

    # Cria o token de acesso com base no usuário autenticado
    token = criar_token(usuario)

    return {
        "access_token": token,
        "token_type": "bearer",
    }
