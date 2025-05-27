# Lu Estilo - API RESTful para Gestão Comercial

## Sobre

Este projeto é uma API RESTful desenvolvida em **FastAPI** para a empresa **Lu Estilo**, voltada para facilitar a comunicação entre o time comercial, clientes e a empresa. A API oferece funcionalidades de gestão de clientes, produtos, pedidos, e autenticação de usuários.

---

## Funcionalidades

- **Autenticação:**
  - Registro de novos usuários
  - Login com JWT e refresh token
  - Controle de acesso com níveis admin e usuário regular

- **Clientes:**
  - CRUD completo com validações de e-mail e CPF únicos
  - Filtros e paginação na listagem

- **Produtos:**
  - CRUD com atributos como descrição, preço, código de barras, seção, estoque, validade e imagens
  - Filtros por categoria, preço e disponibilidade

- **Pedidos:**
  - CRUD com múltiplos produtos por pedido
  - Validação de estoque disponível
  - Filtros por período, seção, status, cliente e ID do pedido

- **Autorização:**
  - Rotas protegidas para usuários autenticados
  - Controle de permissões baseado no tipo de usuário

---

## Tecnologias Utilizadas

- Python 3.10+
- FastAPI
- SQLAlchemy (PostgreSQL)
- Alembic (migrações)
- Pytest (testes unitários e de integração)
- JWT para autenticação
- Docker para containerização

---

## Estrutura do Projeto

```
app/
├── api/                # Rotas e endpoints
├── core/               # Configurações e segurança
├── db/                 # Configuração do banco e migrações
├── models/             # Models SQLAlchemy
├── repositories/       # Repositórios CRUD
├── schemas/            # Schemas Pydantic para validação
├── services/           # Serviços diversos
├── main.py             # Entrada da aplicação
tests/                  # Testes com Pytest
Dockerfile              # Configuração Docker
docker-compose.yml      # Configuração Docker Compose
```

---

## Instalação e Execução

### Pré-requisitos

- Python 3.10+
- Docker e Docker Compose
- Banco de dados PostgreSQL configurado

### Rodando com Docker

Porta padrão da API: **8080**  
URL da documentação: **/docs**

Comando para iniciar o servidor:

```
docker-compose up
docker-compose exec app alembic upgrade head
```

### Rodando Testes Automatizados

```bash
pip install --no-cache-dir -r requirements.txt

python -m pytest
```

### Criar Migration

```bash
alembic revision --autogenerate -m "Migration name"
alembic upgrade head
```

---

## Documentação da API

A documentação interativa está disponível automaticamente via Swagger UI:

```
http://localhost:8080/docs
```

Inclui descrições, exemplos de requisições e respostas para todos os endpoints.


---

**Lu Estilo - API para modernizar as vendas e comunicação do time comercial**
