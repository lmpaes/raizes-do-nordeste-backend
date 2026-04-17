from pydantic import BaseModel


# Dados necessários para cadastro de um produto
class ProdutoCreate(BaseModel):
    nome: str
    descricao: str
    preco: float
    unidade_id: int