# Configuração da conexão com o banco de dados e inicialização do ORM
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Recupera a URL de conexão com o banco
DATABASE_URL = os.getenv("DATABASE_URL")

# Cria o engine responsável pela comunicação com o banco
engine = create_engine(DATABASE_URL, echo=True)

# Configura a sessão que será utilizada nas operações com o banco
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Classe base para os modelos do SQLAlchemy
Base = declarative_base()