# Camada de serviço responsável pelas regras de negócio do pedido
from fastapi import HTTPException

from app.infrastructure.models.pedido_model import Pedido, StatusPedido
from app.infrastructure.models.item_pedido_model import ItemPedido
from app.infrastructure.models.estoque_model import Estoque
from app.infrastructure.models.produto_model import Produto
from app.infrastructure.models.usuario_model import Usuario

from app.core.database import SessionLocal


# Simula um serviço externo de pagamento (mock)
class PaymentService:

    def processar_pagamento(self, valor_total):
        # Regra simples para simular aprovação ou recusa
        if valor_total <= 100:
            return "APROVADO"
        return "RECUSADO"


class PedidoService:

    def criar_pedido(self, usuario_id, unidade_id, canal_pedido, itens):
        # Abre conexão com o banco
        db = SessionLocal()

        valor_total = 0
        itens_pedido = []

        # Percorre os itens do pedido
        for item in itens:
            produto_id = item["produto_id"]
            quantidade = item["quantidade"]

            # Busca o produto
            produto = db.query(Produto).filter(Produto.id == produto_id).first()

            # Valida existência do produto
            if not produto:
                raise HTTPException(
                    status_code=404,
                    detail="PRODUTO_NAO_ENCONTRADO"
                )

            # Verifica o estoque da unidade
            estoque = db.query(Estoque).filter(
                Estoque.produto_id == produto_id,
                Estoque.unidade_id == unidade_id
            ).first()

            # Valida se há estoque suficiente
            if not estoque or estoque.quantidade < quantidade:
                raise HTTPException(
                    status_code=400,
                    detail="ESTOQUE_INSUFICIENTE"
                )

            # Calcula valores do item
            preco_unitario = produto.preco
            subtotal = preco_unitario * quantidade

            valor_total += subtotal

            # Armazena os itens para salvar depois
            itens_pedido.append({
                "produto_id": produto_id,
                "quantidade": quantidade,
                "preco_unitario": preco_unitario,
                "subtotal": subtotal
            })

        # Cria o pedido com status inicial
        pedido = Pedido(
            usuario_id=usuario_id,
            unidade_id=unidade_id,
            canal_pedido=canal_pedido,  # origem do pedido (APP, TOTEM, etc.)
            status=StatusPedido.AGUARDANDO_PAGAMENTO,
            valor_total=valor_total
        )

        db.add(pedido)
        db.commit()
        db.refresh(pedido)

        # Salva os itens do pedido
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

        # Simula integração com serviço externo de pagamento
        payment_service = PaymentService()
        resultado_pagamento = payment_service.processar_pagamento(pedido.valor_total)

        # Atualiza status conforme resultado do pagamento
        if resultado_pagamento == "APROVADO":
            pedido.status = StatusPedido.PAGO

            # Regra simples de fidelidade
            usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
            if usuario:
                usuario.pontos += int(pedido.valor_total)
        else:
            pedido.status = StatusPedido.CANCELADO

        db.commit()
        db.refresh(pedido)

        return pedido