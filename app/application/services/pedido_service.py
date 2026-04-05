from app.infrastructure.models.pedido_model import Pedido, StatusPedido
from app.infrastructure.models.item_pedido_model import ItemPedido
from app.infrastructure.models.estoque_model import Estoque

from app.core.database import SessionLocal


class PedidoService:

    def criar_pedido(self, usuario_id, unidade_id, canal_pedido, itens):
        db = SessionLocal()

        valor_total = 0
        itens_pedido = []

        for item in itens:
            produto_id = item["produto_id"]
            quantidade = item["quantidade"]

            estoque = db.query(Estoque).filter(
                Estoque.produto_id == produto_id,
                Estoque.unidade_id == unidade_id
            ).first()

            if not estoque or estoque.quantidade < quantidade:
                raise Exception("Estoque insuficiente")

            preco_unitario = 10 
            subtotal = preco_unitario * quantidade

            valor_total += subtotal

            itens_pedido.append({
                "produto_id": produto_id,
                "quantidade": quantidade,
                "preco_unitario": preco_unitario,
                "subtotal": subtotal
            })

        pedido = Pedido(
            usuario_id=usuario_id,
            unidade_id=unidade_id,
            canal_pedido=canal_pedido,
            status=StatusPedido.AGUARDANDO_PAGAMENTO,
            valor_total=valor_total
        )

        db.add(pedido)
        db.commit()
        db.refresh(pedido)

        for item in itens_pedido:
            item_pedido = ItemPedido(
                pedido_id=pedido.id,
                produto_id=item["produto_id"],
                quantidade=item["quantidade"],
                preco_unitario=item["preco_unitario"],
                subtotal=item["subtotal"]
            )
            db.add(item_pedido)

        db.commit()
        db.refresh(pedido)
        return pedido