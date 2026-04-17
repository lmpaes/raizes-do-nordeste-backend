# Configuração da conexão com o banco e inicialização do ORM
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL de conexão com o banco de dados
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/raizes_db"

# Cria o engine responsável pela comunicação com o banco
engine = create_engine(DATABASE_URL, echo=True)

# Configuração da sessão utilizada nas operações com o banco
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Classe base para os modelos do SQLAlchemy
Base = declarative_base()