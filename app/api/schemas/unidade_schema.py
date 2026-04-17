from pydantic import BaseModel


# Dados necessários para cadastro de uma unidade
class UnidadeCreate(BaseModel):
    nome: str
    cidade: str
    estado: str