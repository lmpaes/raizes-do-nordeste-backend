from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app.core.database import Base


# Representa os usuários do sistema, incluindo dados de acesso e consentimento de uso de dados
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    senha_hash = Column(String, nullable=False)
    perfil = Column(String, nullable=False)
    consentimento_lgpd = Column(Boolean, nullable=False)
    data_criacao = Column(DateTime, default=datetime.utcnow)
    pontos = Column(Integer, default=0)