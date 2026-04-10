from fastapi import HTTPException

from app.infrastructure.models.pedido_model import Pedido, StatusPedido
from app.infrastructure.models.item_pedido_model import ItemPedido
from app.infrastructure.models.estoque_model import Estoque
from app.infrastructure.models.produto_model import Produto

from app.core.database import SessionLocal


class PaymentService:

    def processar_pagamento(self, valor_total):
        if valor_total <= 100:
            return "APROVADO"
        return "RECUSADO"


class PedidoService:

    def criar_pedido(self, usuario_id, unidade_id, canal_pedido, itens):
        db = SessionLocal()

        valor_total = 0
        itens_pedido = []

        for item in itens:
            produto_id = item["produto_id"]
            quantidade = item["quantidade"]

            produto = db.query(Produto).filter(Produto.id == produto_id).first()

            if not produto:
                raise HTTPException(
                    status_code=404,
                    detail="PRODUTO_NAO_ENCONTRADO"
                )

            estoque = db.query(Estoque).filter(
                Estoque.produto_id == produto_id,
                Estoque.unidade_id == unidade_id
            ).first()

            if not estoque or estoque.quantidade < quantidade:
                raise HTTPException(
                    status_code=400,
                    detail="ESTOQUE_INSUFICIENTE"
                )

            preco_unitario = produto.preco
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

        payment_service = PaymentService()
        resultado_pagamento = payment_service.processar_pagamento(pedido.valor_total)

        if resultado_pagamento == "APROVADO":
            pedido.status = StatusPedido.PAGO
        else:
            pedido.status = StatusPedido.CANCELADO

        db.commit()
        db.refresh(pedido)

        return pedido