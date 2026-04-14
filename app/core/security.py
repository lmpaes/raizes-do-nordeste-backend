# Implementa a geração e validação de tokens para autenticação dos usuários
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from datetime import datetime, timedelta

# Configurações do token JWT
SECRET_KEY = "sua_chave_secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Define o tipo de autenticação via Bearer Token
security = HTTPBearer()


def criar_token(data: dict):
    # Copia os dados que serão armazenados no token
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Adiciona a data de expiração ao token
    to_encode.update({"exp": expire})

    # Gera o token JWT assinado
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        # Decodifica o token recebido na requisição
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")

        # Valida se o token possui as informações esperadas
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )

        # Retorna os dados básicos do usuário autenticado
        return {"user_id": user_id}

    except JWTError:
        # Retorna erro caso o token seja inválido ou expirado
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )