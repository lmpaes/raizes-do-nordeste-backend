# Repositório responsável pelas consultas de produto no banco
from sqlalchemy.orm import Session

from app.infrastructure.models.produto_model import Produto


class ProdutoRepository:
    def get_by_id(self, db: Session, produto_id: int):
        # Busca um produto específico pelo identificador informado
        return db.query(Produto).filter(Produto.id == produto_id).first()
