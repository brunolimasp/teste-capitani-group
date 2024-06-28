FROM python:3.12.2-slim-bookworm

# Adiciona pacotes necessários para compilar dependências Python
RUN apt-get update && apt-get install -y libpq-dev build-essential

# Define o diretório de trabalho dentro do contêiner
WORKDIR /src

# Copia apenas o arquivo de requisitos primeiro
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código-fonte da aplicação para o diretório de trabalho
COPY . .

# Define a porta em que a aplicação irá escutar
EXPOSE 8000


# Cria as tabelas no postgresql
# Roda o servidor uvicorn para servir a aplicação FastAPI na porta 8000
CMD ["sh", "-c", "uvicorn src.main:app --reload & uvicorn src.main:app --host 0.0.0.0 --port 8000"]

