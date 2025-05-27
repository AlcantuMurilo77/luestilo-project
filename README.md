Porta padrão da API: 8080
URL da documentação: /docs

Comando para iniciar o servidor:

```
docker-compose up
docker-compose exec app alembic upgrade head
```

Comando para rodar testes automatizados:

```
pip install --no-cache-dir -r requirements.txt

python -m pytest
```

Criar Migration:

```
alembic revision --autogenerate -m "Migration name"
alembic upgrade head

```
