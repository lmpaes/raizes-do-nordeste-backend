from pydantic import BaseModel


# Dados esperados para realizar o login
class LoginRequest(BaseModel):
    email: str
    senha: str