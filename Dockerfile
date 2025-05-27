FROM python:3

# Define diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos necessários para o container
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
#RUN alembic upgrade head

# Comando padrão ao iniciar o container
EXPOSE 8080
CMD ["fastapi", "dev", "app/main.py", "--host", "0.0.0.0" ,"--port", "8080"] 
