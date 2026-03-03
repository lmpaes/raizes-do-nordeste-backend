from sqlalchemy.orm import Session
from app.infrastructure.models.usuario_model import Usuario


class UsuarioRepository:

    @staticmethod
    def criar(db: Session, usuario: Usuario):
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        return usuario

    @staticmethod
    def buscar_por_email(db: Session, email: str):
        return db.query(Usuario).filter(Usuario.email == email).first()