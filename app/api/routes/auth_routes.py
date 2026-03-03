from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import hashlib

from app.infrastructure.database import get_db
from app.infrastructure.repositories.usuario_repository import UsuarioRepository
from app.core.security import criar_token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login(email: str, senha: str, db: Session = Depends(get_db)):

    usuario = UsuarioRepository.buscar_por_email(db, email)

    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    senha_hash = hashlib.sha256(senha.encode()).hexdigest()

    if usuario.senha_hash != senha_hash:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = criar_token({"sub": usuario.email, "perfil": usuario.perfil})

    return {"access_token": token, "token_type": "bearer"}