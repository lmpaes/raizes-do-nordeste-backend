# Repositório responsável pelas consultas e atualizações de estoque
from sqlalchemy.orm import Session
from app.infrastructure.models.estoque_model import Estoque

class EstoqueRepository:

    def get_by_produto_and_unidade(self, db: Session, produto_id: int, unidade_id: int):
        # Retorna todos os registros de estoque para o produto na unidade
        return db.query(Estoque).filter(
            Estoque.produto_id == produto_id,
            Estoque.unidade_id == unidade_id
        ).order_by(Estoque.id.asc()).all()

    def get_quantidade_total(self, estoques):
        # Soma a quantidade total disponível entre vários registros de estoque
        return sum(estoque.quantidade for estoque in estoques)

    def atualizar_estoque(self, db: Session, estoques, quantidade: int):
        # Valida se a quantidade total disponível é suficiente
        quantidade_disponivel = self.get_quantidade_total(estoques)
        if quantidade_disponivel < quantidade:
            raise ValueError("ESTOQUE_INSUFICIENTE")

        # Consome o estoque de forma sequencial até atender a quantidade pedida
        restante = quantidade

        for estoque in estoques:
            if restante <= 0:
                break

            desconto = min(estoque.quantidade, restante)
            estoque.quantidade -= desconto
            restante -= desconto
            db.add(estoque)

        # Persiste as alterações de quantidade no banco
        db.flush()
