from sqlalchemy import Column, Integer, ForeignKey, DateTime
from datetime import datetime

from app.core.database import Base


class Estoque(Base):
    __tablename__ = "estoques"

    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    unidade_id = Column(Integer, ForeignKey("unidades.id"), nullable=False)
    quantidade = Column(Integer, default=0, nullable=False)
    data_atualizacao = Column(DateTime, default=datetime.utcnow)