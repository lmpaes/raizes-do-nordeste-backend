from sqlalchemy import Column, Integer, ForeignKey, DateTime
from datetime import datetime

from app.core.database import Base


# Representa o programa de fidelidade, armazenando os pontos acumulados por cada usuário
class Fidelidade(Base):
    __tablename__ = "fidelidades"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    pontos = Column(Integer, default=0)
    data_atualizacao = Column(DateTime, default=datetime.utcnow)