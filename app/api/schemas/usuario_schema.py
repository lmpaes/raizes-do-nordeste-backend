# Define os schemas de entrada e saída relacionados ao usuário
from pydantic import BaseModel, EmailStr
from datetime import datetime


# Dados necessários para criação de um novo usuário
class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    perfil: str
    consentimento_lgpd: bool  # Indica se o usuário autorizou o uso dos seus dados


# Dados retornados pela API após operações com usuário
class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr
    perfil: str
    consentimento_lgpd: bool
    data_criacao: datetime

    class Config:
        # Permite converter automaticamente objetos do banco para resposta da API
        from_attributes = True