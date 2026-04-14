# Rotas responsáveis pelo processo de autenticação de usuários (login)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import hashlib

from app.core.database import SessionLocal
from app.infrastructure.repositories.usuario_repository import UsuarioRepository
from app.core.security import criar_token

router = APIRouter(prefix="/auth", tags=["Auth"])


# Cria e encerra a conexão com o banco de dados a cada requisição
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/login")
def login(email: str, senha: str, db: Session = Depends(get_db)):

    # Busca o usuário no banco a partir do e-mail informado
    usuario = UsuarioRepository.buscar_por_email(db, email)

    # Caso o usuário não exista, retorna erro de autenticação
    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    # Gera o hash da senha informada para comparação
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()

    # Verifica se a senha está correta
    if usuario.senha_hash != senha_hash:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    # Cria o token de acesso com dados do usuário
    token = criar_token({"sub": usuario.email, "perfil": usuario.perfil})

    return {"access_token": token, "token_type": "bearer"}