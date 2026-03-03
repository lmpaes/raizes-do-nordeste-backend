from pydantic import BaseModel, EmailStr
from datetime import datetime


class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    perfil: str
    consentimento_lgpd: bool


class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr
    perfil: str
    consentimento_lgpd: bool
    data_criacao: datetime

    class Config:
        from_attributes = True