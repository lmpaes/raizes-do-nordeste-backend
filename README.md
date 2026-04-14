# Raízes do Nordeste API - Backend

## Descrição

API desenvolvida para o Projeto Multidisciplinar da faculdade.

O sistema simula o funcionamento de uma rede de lanchonetes, permitindo:

- Cadastro de usuários
- Autenticação com JWT
- Criação de pedidos
- Validação de estoque
- Processamento de pagamento (mock)
- Atualização de status do pedido

---

## Arquitetura

O projeto foi organizado em camadas:

- API (rotas e controllers)
- Application (regras de negócio)
- Domain (entidades e enums)
- Infrastructure (persistência e banco de dados)

---

## Tecnologias

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT

---

## Pré-requisitos

- Python 3.10 ou superior
- PostgreSQL
- Git

---

## Como rodar o projeto

### 1. Instalar dependências

pip install -r requirements.txt

---

### 2. Criar banco de dados

No PostgreSQL, crie um banco com o nome:

raizes_db

---

### 3. Configurar conexão com o banco

Configure a string de conexão com o banco de dados no projeto, conforme o padrão utilizado no arquivo de configuração.

Exemplo:

postgresql://usuario:senha@localhost:5432/raizes_db

---

### 4. Rodar a aplicação

uvicorn app.main:app --reload

---

## Documentação da API

Após iniciar o projeto, acesse a documentação interativa:

http://127.0.0.1:8000/docs

---

## Autenticação

A API utiliza autenticação via JWT.

Fluxo para autenticação:

1. Criar um usuário no endpoint /usuarios
2. Realizar login no endpoint /auth/login
3. Copiar o token retornado
4. No Swagger, clicar em "Authorize"
5. Inserir o token no formato:

Bearer SEU_TOKEN

---

## Fluxo principal implementado

Fluxo A:

Pedido → Pagamento mock → Atualização de status

Regras de pagamento:

- Valor total menor ou igual a 100: status PAGO
- Valor total maior que 100: status CANCELADO

---

## Testes

O sistema foi validado com cenários de testes cobrindo:

- Cadastro de usuário
- Login
- Criação de pedido
- Pedido com múltiplos itens
- Acesso autenticado
- Acesso sem autenticação (401)
- Login inválido
- Estoque insuficiente
- Pagamento recusado
- Requisição inválida (422)

---

## Estrutura do projeto

app/
 ├── api/
 ├── application/
 ├── domain/
 ├── infrastructure/
 └── core/

---

## Segurança

- Senhas armazenadas com hash
- Autenticação via JWT
- Proteção de endpoints
- Validação de dados de entrada
- Tratamento de erros com padrão consistente

---

## Autor

Leonardo

Projeto acadêmico – UNINTER