# Usa uma imagem oficial do Python levinha
FROM python:3.10-slim

# Evita que o Python grave arquivos .pyc no disco e força o log direto no terminal
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Define a pasta de trabalho dentro do contêiner
WORKDIR /app

# Instala dependências do sistema necessárias para o PostgreSQL
RUN apt-get update \
    && apt-get install -y gcc libpq-dev \
    && apt-get clean

# Copia os requisitos e instala as bibliotecas
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copia o restante do código do projeto para dentro do contêiner
COPY . /app/