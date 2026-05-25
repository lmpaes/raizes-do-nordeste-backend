# Entidade de domínio responsável pelas regras de negócio do pedido
from enum import Enum


class StatusPedido(str, Enum):
    AGUARDANDO_PAGAMENTO = "AGUARDANDO_PAGAMENTO"
    PAGO = "PAGO"
    CANCELADO = "CANCELADO"


class CanalPedidoEnum(str, Enum):
    APP = "APP"
    TOTEM = "TOTEM"
    BALCAO = "BALCAO"
    PICKUP = "PICKUP"
    WEB = "WEB"


class Pedido:
    LIMITE_CANCELAMENTO = 100

    def __init__(self, cliente_id, unidade_id, canal_pedido, itens, total):
        # Normaliza o canal para aceitar enum ou string vinda da camada de entrada
        canal_normalizado = canal_pedido.value if hasattr(canal_pedido, "value") else canal_pedido

        # Garante que o canal informado seja válido para a regra de negócio
        if canal_normalizado not in {canal.value for canal in CanalPedidoEnum}:
            raise ValueError("CANAL_PEDIDO_INVALIDO")

        self.cliente_id = cliente_id
        self.unidade_id = unidade_id
        self.canal_pedido = canal_normalizado
        self.itens = itens
        self.total = total
        self.status = StatusPedido.AGUARDANDO_PAGAMENTO

    def calcular_total(self):
        # Soma o subtotal de todos os itens para formar o total do pedido
        total = 0

        for item in self.itens:
            total += item["quantidade"] * item["preco_unitario"]

        self.total = total
        return total

    def atualizar_status_para_pago(self):
        # Permite a mudança para pago apenas a partir do estado inicial
        if self.status != StatusPedido.AGUARDANDO_PAGAMENTO:
            raise ValueError("TRANSICAO_INVALIDA_STATUS")

        self.status = StatusPedido.PAGO

    def cancelar(self):
        # Impede cancelamento de pedidos que já foram pagos
        if self.status == StatusPedido.PAGO:
            raise ValueError("NAO_PODE_CANCELAR_PEDIDO_PAGO")

        self.status = StatusPedido.CANCELADO

    def processar_regras_negocio(self):
        # Calcula o total antes de aplicar as regras de negócio
        self.calcular_total()

        # Pedidos com valor igual ou superior ao limite são cancelados
        if self.total >= self.LIMITE_CANCELAMENTO:
            self.cancelar()
            return 0

        # Pedidos válidos permanecem pagos e geram pontos iguais ao valor total
        self.atualizar_status_para_pago()
        return int(self.total)

    def deve_baixar_estoque(self):
        # Apenas pedidos pagos devem consumir itens do estoque
        return self.status == StatusPedido.PAGO
