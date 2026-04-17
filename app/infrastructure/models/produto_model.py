from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from datetime import datetime

from app.core.database import Base


# Representa um produto disponível para venda em uma unidade
class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(String)
    preco = Column(Float, nullable=False)
    ativo = Column(Boolean, default=True)
    unidade_id = Column(Integer, ForeignKey("unidades.id"))
    data_criacao = Column(DateTime, default=datetime.utcnow)