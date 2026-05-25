# Modelo responsável por representar a tabela de usuários no banco
from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from app.core.database import Base


class PerfilUsuarioEnum(str, Enum):
    CLIENTE = "CLIENTE"
    ADMIN = "ADMIN"
    GERENTE = "GERENTE"


class Usuario(Base):
    # Estrutura persistida do usuário utilizada pela aplicação
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    senha_hash = Column(String, nullable=False)
    perfil = Column(String, nullable=False, default=PerfilUsuarioEnum.CLIENTE.value)
    consentimento_lgpd = Column(Boolean, nullable=False)
    data_criacao = Column(DateTime, default=datetime.utcnow)
    pontos = Column(Integer, default=0)
