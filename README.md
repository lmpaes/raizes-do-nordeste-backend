# Raízes do Nordeste API - Backend

## Descrição

API desenvolvida para o Projeto Multidisciplinar da faculdade.

O sistema simula o funcionamento de uma rede de lanchonetes, permitindo:

* Cadastro de usuários
* Autenticação com JWT
* Criação de pedidos
* Validação de estoque
* Processamento de pagamento (mock)
* Atualização de status do pedido
* Sistema de fidelidade baseado em pontuação

---

## Arquitetura

O projeto foi organizado em camadas:

* API (rotas e controllers)
* Application (regras de negócio)
* Domain (entidades e enums)
* Infrastructure (persistência e banco de dados)

---

## Tecnologias

* Python
* FastAPI
* PostgreSQL
* SQLAlchemy
* JWT

---

## Pré-requisitos

- Python 3.10 ou superior
- PostgreSQL
- Git

---

## Pré-condições para execução dos testes

Para execução correta dos testes da aplicação, é necessário que alguns dados estejam previamente cadastrados no sistema.

São considerados dados obrigatórios:

* Unidade cadastrada
* Produto vinculado a uma unidade
* Estoque disponível para o produto na unidade

Essas informações são essenciais para garantir o funcionamento adequado do fluxo principal da aplicação, especialmente na criação de pedidos.

A ausência dessas pré-condições pode resultar em erros durante a execução dos testes, como:

* `PRODUTO_NAO_ENCONTRADO`
* `ESTOQUE_INSUFICIENTE`

As pré-condições descritas foram consideradas durante a execução dos testes documentados no projeto.

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

Configure a string de conexão no projeto.

Exemplo:

postgresql://usuario:senha@localhost:5432/raizes_db

---

### 4. Rodar a aplicação

uvicorn app.main:app --reload

---

## Autenticação

A API utiliza autenticação via JWT.

Fluxo para autenticação:

1. Criar um usuário no endpoint `/usuarios`
2. Realizar login no endpoint `/auth/login`
3. Copiar o token retornado
4. No Postman, adicionar no header:

Authorization: Bearer SEU_TOKEN

---

## Fluxo principal implementado

Pedido → Pagamento (mock) → Atualização de status → Fidelidade

---

## Regras de negócio

* O sistema permite a criação de pedidos contendo um ou mais itens vinculados a uma unidade
* O valor total do pedido é calculado com base na soma dos subtotais dos itens (preço do produto × quantidade)
* O pedido é inicialmente criado com status **AGUARDANDO_PAGAMENTO**
* O pagamento é simulado internamente pelo sistema

### Regras de pagamento

* Valor total menor ou igual a 100 → **PAGO**
* Valor total maior que 100 → **CANCELADO**

### Regras de fidelidade

* Apenas pedidos com status **PAGO** geram pontos
* Cada R$1 gasto equivale a **1 ponto de fidelidade**
* Pedidos com status **CANCELADO** não geram pontos

### Validações

* O sistema valida a existência do produto antes de permitir sua inclusão no pedido
* O sistema valida a disponibilidade de estoque na unidade antes de confirmar o pedido
* Caso não haja estoque suficiente, o pedido é rejeitado com erro de **ESTOQUE_INSUFICIENTE**

### Segurança

* O acesso aos endpoints de pedidos requer autenticação via token JWT válido
* Requisições sem autenticação ou com token inválido são bloqueadas

---

## Testes

O sistema foi validado com cenários de testes cobrindo:

* Cadastro de usuário
* Login
* Criação de pedido
* Pedido com múltiplos itens
* Acesso autenticado com JWT
* Acesso sem autenticação (401)
* Login com credenciais inválidas
* Estoque insuficiente
* Pagamento recusado
* Requisição inválida (422)

---

## Documentação da API

A documentação automática do FastAPI pode ser acessada em:

http://127.0.0.1:8000/docs

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

* Senhas armazenadas com hash
* Autenticação via JWT
* Proteção de endpoints
* Validação de dados de entrada
* Tratamento de erros padronizado

---

## Autor

Leonardo

Projeto acadêmico – UNINTER