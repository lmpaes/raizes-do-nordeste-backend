# Configuração simples de logging para uso geral da aplicação
import logging

# Define formato e nível padrão dos logs exibidos no terminal
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Cria uma instância única de logger reutilizável no projeto
logger = logging.getLogger("app")
