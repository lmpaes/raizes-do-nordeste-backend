# Camada de segurança responsável por gerar e validar tokens JWT
import os
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.infrastructure.models.usuario_model import Usuario

SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE_ME")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

security = HTTPBearer()


def criar_token(usuario: Usuario) -> str:
    # Define o tempo de expiração do token
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Monta o payload com os dados mínimos para autenticação
    payload = {
        "sub": str(usuario.id),
        "perfil": usuario.perfil,
        "exp": expire,
    }

    # Gera o JWT assinado com a chave secreta da aplicação
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    # Extrai o token enviado no header Authorization
    token = credentials.credentials

    try:
        # Decodifica o token e recupera o identificador do usuário
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_identifier = payload.get("sub")

        # Garante que o token contenha o identificador do usuário
        if not user_identifier:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="TOKEN_INVALIDO",
            )

        # Converte o identificador para inteiro antes da busca no banco
        user_id = int(user_identifier)
    except (JWTError, ValueError, TypeError):
        # Retorna erro padrão quando o token estiver inválido ou malformado
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="TOKEN_INVALIDO",
        )

    # Busca o usuário autenticado no banco com base no id do token
    usuario = db.query(Usuario).filter(Usuario.id == user_id).first()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="USUARIO_NAO_ENCONTRADO",
        )

    return usuario


def require_roles(*roles):
    # Cria uma validação reutilizável de perfis permitidos no endpoint
    def role_checker(current_user: Usuario = Depends(get_current_user)):
        # Impede acesso quando o perfil do usuário não estiver na lista permitida
        if current_user.perfil not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="SEM_PERMISSAO",
            )
        return current_user

    return role_checker
