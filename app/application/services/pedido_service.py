# Camada de serviço responsável por orquestrar criação de pedidos
from datetime import datetime

from sqlalchemy.orm import Session

from app.domain.entities.pedido import Pedido as PedidoDomain, StatusPedido as PedidoStatusDomain

from app.infrastructure.models.pedido_model import (
    Pedido as PedidoModel,
    StatusPedido as PedidoStatusModel,
    CanalPedido as PedidoCanalModel,
)
from app.infrastructure.models.item_pedido_model import ItemPedido as PedidoItemModel
from app.infrastructure.models.fidelidade_model import Fidelidade
from app.infrastructure.models.usuario_model import Usuario

from app.infrastructure.repositories.produto_repository import ProdutoRepository
from app.infrastructure.repositories.estoque_repository import EstoqueRepository

from app.domain.exceptions import (
    ProdutoNaoEncontrado,
    EstoqueInsuficiente,
    DomainException
)

from app.core.logger import logger


class PedidoService:

    def __init__(self):
        self.produto_repo = ProdutoRepository()
        self.estoque_repo = EstoqueRepository()

    def criar_pedido(self, db: Session, dados_pedido, usuario_id: int):
        try:
            logger.info(
                f"Inicio criacao pedido - usuario={usuario_id} "
                f"unidade={dados_pedido.unidade_id} canal={dados_pedido.canal_pedido}"
            )

            # Prepara os itens validados e o mapa de estoque por produto
            itens_processados = []
            estoques_map = {}

            for item in dados_pedido.itens:
                # Busca o produto solicitado no pedido
                produto = self.produto_repo.get_by_id(db, item.produto_id)

                if not produto:
                    raise ProdutoNaoEncontrado()

                # Recupera todos os registros de estoque do produto na unidade
                estoques = self.estoque_repo.get_by_produto_and_unidade(
                    db,
                    produto.id,
                    dados_pedido.unidade_id
                )

                if not estoques:
                    raise ProdutoNaoEncontrado()

                # Soma a quantidade disponível para validar se o pedido pode ser criado
                quantidade_disponivel = self.estoque_repo.get_quantidade_total(estoques)

                if quantidade_disponivel < item.quantidade:
                    raise EstoqueInsuficiente()

                estoques_map[produto.id] = estoques

                itens_processados.append({
                    "produto_id": produto.id,
                    "quantidade": item.quantidade,
                    "preco_unitario": produto.preco,
                    "subtotal": item.quantidade * produto.preco,
                })

            # Cria a entidade de domínio que concentra as regras do pedido
            pedido_domain = PedidoDomain(
                cliente_id=usuario_id,
                unidade_id=dados_pedido.unidade_id,
                canal_pedido=dados_pedido.canal_pedido,
                itens=itens_processados,
                total=0
            )

            # Processa as regras de negócio e obtém os pontos gerados pelo pedido
            pontos_gerados = pedido_domain.processar_regras_negocio()

            # Atualiza pontos do usuário apenas quando o pedido for pago
            if pedido_domain.status == PedidoStatusDomain.PAGO:
                usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
                if usuario:
                    usuario.pontos = (usuario.pontos or 0) + pontos_gerados
                    db.add(usuario)

                # Atualiza ou cria o registro de fidelidade do usuário
                fidelidade = db.query(Fidelidade).filter(Fidelidade.usuario_id == usuario_id).first()
                if fidelidade:
                    fidelidade.pontos = (fidelidade.pontos or 0) + pontos_gerados
                    fidelidade.data_atualizacao = datetime.utcnow()
                else:
                    fidelidade = Fidelidade(
                        usuario_id=usuario_id,
                        pontos=pontos_gerados,
                    )

                db.add(fidelidade)

            # Converte a entidade de domínio para o modelo persistido no banco
            pedido_model = PedidoModel(
                usuario_id=usuario_id,
                unidade_id=pedido_domain.unidade_id,
                canal_pedido=PedidoCanalModel(pedido_domain.canal_pedido),
                status=PedidoStatusModel(pedido_domain.status.value),
                valor_total=pedido_domain.total,
            )

            db.add(pedido_model)
            db.flush()

            for item in itens_processados:
                # Salva cada item pertencente ao pedido criado
                pedido_item = PedidoItemModel(
                    pedido_id=pedido_model.id,
                    produto_id=item["produto_id"],
                    quantidade=item["quantidade"],
                    preco_unitario=item["preco_unitario"],
                    subtotal=item["subtotal"],
                )
                db.add(pedido_item)

                # Dá baixa no estoque somente para pedidos pagos
                if pedido_domain.deve_baixar_estoque():
                    estoques = estoques_map[item["produto_id"]]

                    self.estoque_repo.atualizar_estoque(
                        db,
                        estoques,
                        item["quantidade"]
                    )

            # Confirma a transação e devolve o pedido persistido
            db.commit()
            db.refresh(pedido_model)
            pedido_model.pontos_gerados = pontos_gerados

            return pedido_model

        except DomainException:
            # Desfaz a transação quando a regra de negócio lançar erro conhecido
            db.rollback()
            raise

        except Exception:
            # Converte erros inesperados em erro de domínio padronizado
            db.rollback()
            raise DomainException(
                error="ERRO_INTERNO",
                message="Erro interno do servidor.",
                status_code=500
            )
