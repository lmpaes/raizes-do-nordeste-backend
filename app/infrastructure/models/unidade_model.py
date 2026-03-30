from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime

from app.core.database import Base


class Unidade(Base):
    __tablename__ = "unidades"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cidade = Column(String, nullable=False)
    estado = Column(String(2), nullable=False)

    ativa = Column(Boolean, default=True)
    data_criacao = Column(DateTime, default=datetime.utcnow)