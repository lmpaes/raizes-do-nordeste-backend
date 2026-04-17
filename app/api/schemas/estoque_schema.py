from pydantic import BaseModel


# Dados necessários para registrar estoque de um produto em uma unidade
class EstoqueCreate(BaseModel):
    produto_id: int
    unidade_id: int
    quantidade: int