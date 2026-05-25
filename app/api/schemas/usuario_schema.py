# Schemas responsáveis por validar entrada e saída de dados do usuário
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr


class PerfilUsuarioEnum(str, Enum):
    CLIENTE = "CLIENTE"
    ADMIN = "ADMIN"
    GERENTE = "GERENTE"

    # Dados obrigatórios para cadastrar um novo usuário
class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    perfil: PerfilUsuarioEnum
    consentimento_lgpd: bool

    # Dados retornados pela API após operações com usuário
class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr
    perfil: PerfilUsuarioEnum
    consentimento_lgpd: bool
    data_criacao: datetime

    # Permite converter automaticamente objetos ORM em resposta da API
    class Config:
        from_attributes = True
