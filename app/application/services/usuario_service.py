# Camada de serviço responsável pelas regras de negócio relacionadas ao usuário
from sqlalchemy.orm import Session
import hashlib

from app.infrastructure.models.usuario_model import Usuario
from app.infrastructure.repositories.usuario_repository import UsuarioRepository
from app.api.schemas.usuario_schema import UsuarioCreate


# Gera o hash da senha antes de armazenar no banco
def gerar_hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode()).hexdigest()


class UsuarioService:

    @staticmethod
    def criar_usuario(db: Session, usuario_data: UsuarioCreate):

        # Verifica se já existe um usuário com o mesmo e-mail
        usuario_existente = UsuarioRepository.buscar_por_email(db, usuario_data.email)
        if usuario_existente:
            raise ValueError("Email já cadastrado")

        # Aplica hash na senha para não armazenar o valor em texto puro
        senha_hash = gerar_hash_senha(usuario_data.senha)

        # Cria o objeto de usuário com os dados recebidos
        novo_usuario = Usuario(
            nome=usuario_data.nome,
            email=usuario_data.email,
            senha_hash=senha_hash,
            perfil=usuario_data.perfil,
            consentimento_lgpd=usuario_data.consentimento_lgpd
        )

        # Persiste o usuário no banco de dados
        return UsuarioRepository.criar(db, novo_usuario)