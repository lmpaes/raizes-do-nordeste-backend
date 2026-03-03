from sqlalchemy.orm import Session
import hashlib

from app.infrastructure.models.usuario_model import Usuario
from app.infrastructure.repositories.usuario_repository import UsuarioRepository
from app.api.schemas.usuario_schema import UsuarioCreate


def gerar_hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode()).hexdigest()


class UsuarioService:

    @staticmethod
    def criar_usuario(db: Session, usuario_data: UsuarioCreate):

        usuario_existente = UsuarioRepository.buscar_por_email(db, usuario_data.email)
        if usuario_existente:
            raise ValueError("Email já cadastrado")

        senha_hash = gerar_hash_senha(usuario_data.senha)

        novo_usuario = Usuario(
            nome=usuario_data.nome,
            email=usuario_data.email,
            senha_hash=senha_hash,
            perfil=usuario_data.perfil,
            consentimento_lgpd=usuario_data.consentimento_lgpd
        )

        return UsuarioRepository.criar(db, novo_usuario)