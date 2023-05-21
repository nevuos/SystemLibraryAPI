# Use a imagem oficial do Python 3.8 como base
FROM python:3.8-slim-buster

# Configurar o diretório de trabalho
WORKDIR /SystemLibraryApi

# Instalar as dependências de sistema
RUN apt-get update \
    && apt-get install -y build-essential tclsh pkg-config libssl-dev libsqlite3-dev git libffi-dev python3-dev curl \
    && rm -rf /var/lib/apt/lists/*

# Clonar o repositório do sqlcipher
RUN git clone https://github.com/sqlcipher/sqlcipher.git \
    && cd sqlcipher \
    && ./configure --enable-tempstore=yes CFLAGS="-DSQLITE_HAS_CODEC" LDFLAGS="-lcrypto" \
    && make \
    && make install \
    && cd ..

# Instalar o pip
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
    && python get-pip.py \
    && rm get-pip.py

# Copiar os arquivos de requirements para o diretório de trabalho
COPY requirements.txt .

# Instalar as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Instalar o pysqlcipher3
RUN pip install pysqlcipher3

# Copiar o código fonte do projeto para o diretório de trabalho
COPY . .

# Definir o comando de inicialização do contêiner
CMD [ "python", "./run.py" ]
