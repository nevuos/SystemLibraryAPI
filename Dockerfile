# Use a imagem oficial do Python 3.8 como base
FROM python:3.8-slim-buster

# Definir o diretório de trabalho no Docker
WORKDIR /app

# Copiar os arquivos de requisitos para o contêiner
COPY requirements.txt requirements.txt

# Instalar as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copiar os arquivos do projeto para o contêiner
COPY . .

# Expõe a porta que o Flask vai usar
EXPOSE 8080

# Define o comando para executar o projeto
CMD [ "python", "./run.py" ]
