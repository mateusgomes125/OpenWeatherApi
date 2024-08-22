# Usando uma imagem oficial do Python como base
FROM python:3.10-slim

# Definindo o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copiando o arquivo de requisitos e instalando as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiando o código da aplicação para o contêiner
COPY . .

# Definindo a variável de ambiente para o Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expondo a porta em que o Flask estará rodando
EXPOSE 5000

# Comando para rodar a aplicação
CMD ["flask", "run"]
