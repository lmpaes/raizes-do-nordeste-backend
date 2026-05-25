# Exceções de domínio responsáveis por padronizar erros de negócio da aplicação
from datetime import datetime


class DomainException(Exception):
    # Classe base para erros conhecidos tratados pela aplicação
    def __init__(self, error: str, message: str, status_code: int = 400, details: list = None):
        self.error = error
        self.message = message
        self.status_code = status_code
        self.details = details or []
        super().__init__(message)


class ProdutoNaoEncontrado(DomainException):
    # Erro utilizado quando o produto informado não existe no fluxo de negócio
    def __init__(self):
        super().__init__(
            error="PRODUTO_NAO_ENCONTRADO",
            message="Produto não encontrado.",
            status_code=404
        )


class EstoqueInsuficiente(DomainException):
    # Erro utilizado quando a quantidade pedida é maior que o saldo disponível
    def __init__(self):
        super().__init__(
            error="ESTOQUE_INSUFICIENTE",
            message="Não há quantidade suficiente em estoque.",
            status_code=409
        )


def formatar_erro(ex: DomainException, path: str):
    # Monta o payload padrão de erro retornado pela API
    return {
        "error": ex.error,
        "message": ex.message,
        "details": ex.details,
        "timestamp": datetime.utcnow().isoformat(),
        "path": path
    }
