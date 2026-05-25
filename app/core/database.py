# Configuração central de conexão e sessão com o banco de dados
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Define a URL utilizada para conexão com o banco
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/raizes_db"

# Cria o engine responsável pela comunicação com o banco
engine = create_engine(DATABASE_URL, echo=True)

# Configura a sessão utilizada nas operações com o banco
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Define a classe base usada pelos modelos do SQLAlchemy
Base = declarative_base()


# Abre e fecha a sessão do banco a cada requisição
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
